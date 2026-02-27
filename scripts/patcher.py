import os
import re

# Directory containing your .smali patch files
PATCH_DIR = os.path.join("scripts", "smali")
# Directory where Apktool decompiles the JAR
OUT_DIR = "out_folder"

def apply_patch(target_file_keyword, method_name, patch_file_name):
    patch_path = os.path.join(PATCH_DIR, patch_file_name)
    
    if not os.path.exists(patch_path):
        print(f"❌ Patch file not found: {patch_file_name}")
        return

    with open(patch_path, 'r') as f:
        new_method_body = f.read()

    found = False
    # Search recursively through all smali folders (smali, smali_classes2, etc.)
    for root, dirs, files in os.walk(OUT_DIR):
        for file in files:
            if target_file_keyword in file and file.endswith(".smali"):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                
                # Regex to find the block from .method to .end method containing the method_name
                pattern = re.compile(rf'\.method.*?{re.escape(method_name)}.*?\.end method', re.DOTALL)
                
                if pattern.search(content):
                    updated = pattern.sub(new_method_body, content)
                    with open(path, 'w') as f:
                        f.write(updated)
                    print(f"✅ Successfully Patched: {file} -> {method_name}")
                    found = True
    
    if not found:
        print(f"⚠️ Method {method_name} not found in {target_file_keyword}")

# --- PATCH EXECUTION LIST ---

# FaceService Patches
apply_patch("FaceService", "getDeclaredInstances", "getDeclaredInstances.smali")

# FaceProvider Patches
apply_patch("FaceProvider", "initSensors", "initSensors.smali")
apply_patch("FaceProvider", "cancelAuthentication", "cancelAuthentication.smali")
apply_patch("FaceProvider", "cancelEnrollment", "cancelEnrollment.smali")
apply_patch("FaceProvider", "getAuthenticatorId", "getAuthenticatorId.smali")
apply_patch("FaceProvider", "getEnrolledFaces", "getEnrolledFaces.smali")
apply_patch("FaceProvider", "isHardwareDetected", "isHardwareDetected.smali")
apply_patch("FaceProvider", "scheduleAuthenticate", "scheduleAuthenticate.smali")
apply_patch("FaceProvider", "scheduleEnroll", "scheduleEnroll.smali")
apply_patch("FaceProvider", "scheduleGenerateChallenge", "scheduleGenerateChallenge.smali")
apply_patch("FaceProvider", "scheduleRemove", "scheduleRemove.smali")
apply_patch("FaceProvider", "scheduleRevokeChallenge", "scheduleRevokeChallenge.smali")
apply_patch("FaceProvider", "lambda$new$2", "FaceProvider.smali") 

# Secure Screenshot Patches
apply_patch("WindowManagerService", "notifyScreenshotListeners", "notifyScreenshotListeners.smali")
apply_patch("WindowState", "isSecureLocked", "isSecureLocked.smali")
