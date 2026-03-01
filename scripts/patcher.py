import os
import re

# Directory containing your .smali patch files
PATCH_DIR = os.path.join("scripts", "smali")
# Directory where Apktool decompiles the JAR
OUT_DIR = "out_folder"

# Read env variable for optional patches
DISABLE_SECURE_SCREENSHOT = os.environ.get("DISABLE_SECURE_SCREENSHOT", "false").lower() == "true"

def find_target_files(target_file_keyword, prefer_aidl=False):
    """Find all matching smali files, optionally preferring aidl path."""
    matches = []
    for root, dirs, files in os.walk(OUT_DIR):
        for file in files:
            if target_file_keyword in file and file.endswith(".smali"):
                matches.append(os.path.join(root, file))
    
    if not matches:
        return []
    
    if prefer_aidl and len(matches) > 1:
        aidl_matches = [p for p in matches if "aidl" in p]
        if aidl_matches:
            return aidl_matches
    
    return matches

def apply_patch(target_file_keyword, method_name, patch_file_name, prefer_aidl=False):
    patch_path = os.path.join(PATCH_DIR, patch_file_name)
    
    if not os.path.exists(patch_path):
        print(f"❌ Patch file not found: {patch_file_name}")
        return

    with open(patch_path, 'r') as f:
        new_method_body = f.read().strip()

    found = False
    targets = find_target_files(target_file_keyword, prefer_aidl=prefer_aidl)

    for path in targets:
        with open(path, 'r') as f:
            content = f.read()
        
        pattern = re.compile(rf'\.method.*?{re.escape(method_name)}.*?\.end method', re.DOTALL)
        
        if pattern.search(content):
            updated = pattern.sub(new_method_body, content)
            with open(path, 'w') as f:
                f.write(updated)
            print(f"✅ Successfully Patched: {os.path.basename(path)} -> {method_name}")
            found = True
    
    if not found:
        print(f"⚠️ Method '{method_name}' not found in '{target_file_keyword}'")

# --- PATCH EXECUTION LIST ---

# FaceService Patches
apply_patch("FaceService", "getDeclaredInstances", "getDeclaredInstances.smali")

# FaceProvider Patches (prefer aidl path)
apply_patch("FaceProvider", "initSensors", "initSensors.smali", prefer_aidl=True)
apply_patch("FaceProvider", "cancelAuthentication", "cancelAuthentication.smali", prefer_aidl=True)
apply_patch("FaceProvider", "cancelEnrollment", "cancelEnrollment.smali", prefer_aidl=True)
apply_patch("FaceProvider", "getAuthenticatorId", "getAuthenticatorId.smali", prefer_aidl=True)
apply_patch("FaceProvider", "getEnrolledFaces", "getEnrolledFaces.smali", prefer_aidl=True)
apply_patch("FaceProvider", "isHardwareDetected", "isHardwareDetected.smali", prefer_aidl=True)
apply_patch("FaceProvider", "scheduleAuthenticate", "scheduleAuthenticate.smali", prefer_aidl=True)
apply_patch("FaceProvider", "scheduleEnroll", "scheduleEnroll.smali", prefer_aidl=True)
apply_patch("FaceProvider", "scheduleGenerateChallenge", "scheduleGenerateChallenge.smali", prefer_aidl=True)
apply_patch("FaceProvider", "scheduleRemove", "scheduleRemove.smali", prefer_aidl=True)
apply_patch("FaceProvider", "scheduleRevokeChallenge", "scheduleRevokeChallenge.smali", prefer_aidl=True)
apply_patch("FaceProvider", "lambda$new$2", "FaceProvider.smali", prefer_aidl=True)

# Secure Screenshot Patches (optional)
if DISABLE_SECURE_SCREENSHOT:
    print("📸 Applying Disable Secure Screenshot patches...")
    apply_patch("WindowManagerService", "notifyScreenshotListeners", "notifyScreenshotListeners.smali")
    apply_patch("WindowState", "isSecureLocked", "isSecureLocked.smali")
else:
    print("⏭️ Skipping Disable Secure Screenshot patches")
