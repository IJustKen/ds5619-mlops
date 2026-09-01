"""
A tiny local model registry — enough to demonstrate the governance ideas from
this week's lecture without needing an MLflow/W&B server:

  1. The registry as an artifact store (register_model) — one immutable,
     named version per trained model, not forty nearly-identical runs.
  2. The model card as the governance control (generate_model_card) — must
     actually be filled in, not just present.
  3. Promotion between stages (promote_model) as a GATE, not a rename — you
     cannot reach Production without a complete card and metrics that clear
     the bar. Promoting a new model to Production auto-archives whichever
     version was there before, so "what's in production" always has exactly
     one answer.

Fill in the four functions marked # TODO. Helpers/constants above them are
done.
"""
import json
import os
from datetime import datetime, timezone

PRODUCTION_F1_THRESHOLD = 0.70
REQUIRED_CARD_FIELDS = ["intended_use", "training_data", "limitations", "ethical_considerations"]


class GovernanceError(Exception):
    """Raised when a promotion is attempted that violates a governance rule."""


def _now():
    return datetime.now(timezone.utc).isoformat()


def _next_version_id(existing_dir):
    """Given a directory of existing v1/, v2/, ... subfolders, return the
    next version id string. Given — you don't need to touch this."""
    if not os.path.isdir(existing_dir):
        return "v1"
    nums = []
    for name in os.listdir(existing_dir):
        if name.startswith("v") and name[1:].isdigit():
            nums.append(int(name[1:]))
    return f"v{max(nums, default=0) + 1}"


def _model_dir(registry_dir, name, version_id):
    return os.path.join(registry_dir, "models", name, version_id)


# ---------------------------------------------------------------------------
# Part 1 — Register a model version (the artifact store)
# ---------------------------------------------------------------------------

def register_model(name, model_path, metrics, registry_dir):
    """Register a new version of model `name` in the registry.

    Steps:
      1. Allocate version_id via _next_version_id(os.path.join(registry_dir,
         "models", name)).
      2. Create _model_dir(registry_dir, name, version_id).
      3. Copy the model file's contents into that directory as "model.json"
         (read model_path as JSON, write it back out — this is your
         "artifact").
      4. Write manifest.json in that directory with at least these keys:
           version_id, name, metrics (the dict you were given, as-is),
           stage (str, initial value "None" — matches the convention that a
           freshly-registered model isn't in any deployment stage yet),
           created_at (use _now()).
      5. Return version_id (str).
    """
    version_id = _next_version_id(os.path.join(registry_dir,"models", name))
    model_dir = _model_dir(registry_dir, name, version_id)
    
    os.makedirs(model_dir, exist_ok=True)   # create the directory

    # Read model JSON and copy paste to the registry's 
    # appropriate directory
    with open(model_path, "r") as f:
        model = json.load(f)    # copy from original model .json file

    artifact_path = os.path.join(model_dir, "model.json")
    with open(artifact_path, "w") as f:
        json.dump(model, f, indent=2)   # basically pasting from original model .json file

    # Create manifest for this model
    manifest = {
        "version_id": version_id,
        "name": name,
        "metrics": metrics,
        "stage": "None",
        "created_at": _now(),
    }

    # create the manifest.json file for this model
    manifest_path = os.path.join(model_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Return version ID as asked
    return version_id


# ---------------------------------------------------------------------------
# Part 2 — Generate a model card (must be genuinely filled in, not just present)
# ---------------------------------------------------------------------------

def generate_model_card(name, version_id, card_fields, registry_dir):
    """Validate and write a model card for an already-registered model
    version.

    `card_fields` is a dict that should contain every key in
    REQUIRED_CARD_FIELDS, each mapped to a non-empty string that does NOT
    contain the literal substring "TODO" (a card with a TODO in it isn't
    actually filled in — reject it).

    Steps:
      1. For each key in REQUIRED_CARD_FIELDS: if it's missing from
         card_fields, or its value is empty/whitespace-only, or its value
         contains "TODO", raise ValueError naming the offending field.
      2. Read the version's existing manifest.json (from _model_dir(...)) to
         pull in its "metrics" for the card.
      3. Write model_card.json into _model_dir(registry_dir, name,
         version_id) containing: name, version_id, the fields from
         card_fields, metrics (from step 2), created_at (use _now()).
      4. Return the path you wrote to.
    """
    # Validate the required card fields
    for field in REQUIRED_CARD_FIELDS:
        if field not in card_fields:
            raise ValueError(f"Missing required field: {field}")

        value = card_fields[field]

        if not value.strip():   # check for empty/whitespace-only string
            raise ValueError(f"Invalid value for field: {field}")

        if "TODO" in value: # check for value being == "TODO", basically field has not been filled yet
            raise ValueError(f"TODO found in field: {field}")

    # Read the existing manifest.json
    model_dir = _model_dir(registry_dir, name, version_id)
    manifest_path = os.path.join(model_dir, "manifest.json")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    metrics = manifest["metrics"]

    # Create and write model card
    model_card = {
        "name": name,
        "version_id": version_id,
        "metrics": metrics,
        "created_at": _now()
    }
    # fields from card_fields also should be included
    for k,v in card_fields.items():
        model_card[k] = v

    card_path = os.path.join(model_dir, "model_card.json")

    with open(card_path, "w") as f:
        json.dump(model_card, f, indent=2)

    # Return the path
    return card_path


# ---------------------------------------------------------------------------
# Part 3 — Promote a model version (the governance gate)
# ---------------------------------------------------------------------------

def promote_model(name, version_id, target_stage, registry_dir):
    """Move model `name` version `version_id` to `target_stage`
    ("Staging" or "Production").

    Governance rule enforced HERE, not just documented: promoting to
    "Production" requires BOTH of:
      (a) a model_card.json exists for this version (use
          os.path.exists(os.path.join(_model_dir(...), "model_card.json"))).
      (b) this version's metrics["f1"] >= PRODUCTION_F1_THRESHOLD (read
          metrics from its manifest.json).
    If either fails, raise GovernanceError with a message saying which
    condition failed. Promotion to "Staging" has no such gate.

    On a successful promotion to "Production": if any OTHER version of the
    same model `name` currently has stage == "Production", set that other
    version's stage to "Archived" first (so there is at most one Production
    version at a time — write its updated manifest.json back to disk).

    Then:
      1. Update this version's manifest.json: set "stage" to target_stage.
      2. Append an entry {"from_stage": <old stage>, "to_stage":
         target_stage, "at": _now()} to a list under manifest["history"]
         (create the list if it doesn't exist yet — never overwrite earlier
         entries, this is the audit trail).
      3. Write the updated manifest.json back to disk.
      4. Return the updated manifest (dict).
    """
    # Get this model version's directory and manifest.json file
    model_dir = _model_dir(registry_dir, name, version_id)
    manifest_path = os.path.join(model_dir, "manifest.json")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # Governance checks for promoting to Production
    if target_stage == "Production":

        # Check (a) model card exists
        card_path = os.path.join(model_dir, "model_card.json")

        if not os.path.exists(card_path):
            raise GovernanceError("Production promotion failed - model card file does not exist")

        # Check (b) F1 threshold
        f1 = manifest["metrics"]["f1"]

        if f1 < PRODUCTION_F1_THRESHOLD:
            raise GovernanceError(f"Production promotion failed: model's f1 ({f1}) is below "
                f"the required threshold ({PRODUCTION_F1_THRESHOLD})")

    # If promoting to Production, archive any existing Production version
    if target_stage == "Production":

        models_dir = os.path.join(registry_dir, "models", name)

        if os.path.exists(models_dir):
            for other_version in os.listdir(models_dir):

                # Don't archive the version we're promoting
                if other_version == version_id:
                    continue

                other_dir = os.path.join(models_dir, other_version)
                other_manifest_path = os.path.join(other_dir, "manifest.json")

                # Checking if directory even has a manifest
                if not os.path.isfile(other_manifest_path):
                    continue

                with open(other_manifest_path, "r") as f:
                    other_manifest = json.load(f)

                # archive previous production model(s)
                if other_manifest.get("stage") == "Production":
                    other_manifest["stage"] = "Archived"

                    with open(other_manifest_path, "w") as f:
                        json.dump(other_manifest, f, indent=2)

    # Update this version's stage and audit history
    old_stage = manifest["stage"]

    manifest["stage"] = target_stage

    if "history" not in manifest:   # append a history to the manifest 
        manifest["history"] = []

    manifest["history"].append({"from_stage": old_stage, "to_stage": target_stage, "at": _now()})

    # Write updated manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest


# ---------------------------------------------------------------------------
# Part 4 — Look up what's currently in production
# ---------------------------------------------------------------------------

def get_production_model(name, registry_dir):
    """Return the manifest (dict) of whichever version of model `name` is
    currently in stage "Production", by scanning every version's
    manifest.json under registry_dir/models/{name}/.

    Return None if no version is currently in Production.
    """
    models_dir = os.path.join(registry_dir, "models", name)

    if not os.path.exists(models_dir):  # no such model name exists only
        return None

    for version_id in os.listdir(models_dir):
        version_dir = os.path.join(models_dir, version_id)
        manifest_path = os.path.join(version_dir, "manifest.json")  # get path for each manifest.json file

        if not os.path.isfile(manifest_path):
            continue    # file does not exist at means we check the next version

        with open(manifest_path, "r") as f:
            manifest = json.load(f)     

        if manifest.get("stage") == "Production":
            return manifest     # return the manifest of the model name and version which is in production

    return None     # nothing found so return None
