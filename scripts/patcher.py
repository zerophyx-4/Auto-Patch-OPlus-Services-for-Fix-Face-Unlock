import os
import re

def patch_method(file_name, method_signature, new_body):
    """
    Mencari file smali dan mengganti seluruh isi method berdasarkan signature-nya.
    """
    for root, dirs, files in os.walk("out_smali"):
        if file_name in files:
            path = os.path.join(root, file_name)
            with open(path, 'r') as f:
                content = f.read()
            
            # Regex untuk menangkap method secara utuh dari .method sampai .end method
            # Menggunakan re.escape pada signature agar karakter khusus seperti $ atau [ tidak error
            pattern = re.compile(rf'\.method.*?{re.escape(method_signature)}.*?\.end method', re.DOTALL)
            
            if pattern.search(content):
                updated = pattern.sub(new_body, content)
                with open(path, 'w') as f:
                    f.write(updated)
                print(f"✅ Berhasil Patch: {file_name} -> {method_signature}")
                return
    print(f"❌ Gagal: {file_name} atau method {method_signature} tidak ditemukan.")

# --- 1. INITIALIZE BRIDGE (FaceService & FaceProvider) ---

patch_method("FaceService.smali", "getDeclaredInstances()[Ljava/lang/String;", 
""".method public static getDeclaredInstances()[Ljava/lang/String;
    .registers 3
    const/4 v0, 0x1
    new-array v0, v0, [Ljava/lang/String;
    const-string v1, "default"
    const/4 v2, 0x0
    aput-object v1, v0, v2
    return-object v0
.end method""")

patch_method("FaceProvider.smali", "initSensors(Z[Landroid/hardware/biometrics/face/SensorProps;)V",
""".method private initSensors(Z[Landroid/hardware/biometrics/face/SensorProps;)V
    .registers 12
    iget-object v0, p0, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;->mContext:Landroid/content/Context;
    invoke-static {v0}, Lax/nd/faceunlock/FaceAuthBridge;->init(Landroid/content/Context;)V
    new-instance v0, Landroid/hardware/biometrics/face/SensorProps;
    invoke-direct {v0}, Landroid/hardware/biometrics/face/SensorProps;-><init>()V
    new-instance v1, Landroid/hardware/biometrics/common/CommonProps;
    invoke-direct {v1}, Landroid/hardware/biometrics/common/CommonProps;-><init>()V
    const/4 v2, 0x1
    iput v2, v1, Landroid/hardware/biometrics/common/CommonProps;->sensorId:I
    iput-object v1, v0, Landroid/hardware/biometrics/face/SensorProps;->commonProps:Landroid/hardware/biometrics/common/CommonProps;
    const/4 v1, 0x0
    invoke-direct {p0, v0, v1}, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;->addAidlSensors(Landroid/hardware/biometrics/face/SensorProps;Z)V
    invoke-static {}, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;->getExtImpl()Lcom/android/server/biometrics/sensors/face/aidl/IFaceProviderExt;
    move-result-object v2
    move-object v3, p0
    iget-object v4, p0, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;->mContext:Landroid/content/Context;
    const/4 v1, 0x1
    new-array v5, v1, [Landroid/hardware/biometrics/face/SensorProps;
    const/4 v1, 0x0
    aput-object v0, v5, v1
    iget-object v6, p0, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;->mHalInstanceName:Ljava/lang/String;
    iget-object v7, p0, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;->mHandler:Landroid/os/Handler;
    invoke-interface/range {v2 .. v7}, Lcom/android/server/biometrics/sensors/face/aidl/IFaceProviderExt;->init(Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;Landroid/content/Context;[Landroid/hardware/biometrics/face/SensorProps;Ljava/lang/String;Landroid/os/Handler;)V
    return-void
.end method""")

# --- 2. REPLACE FACE PROVIDER METHODS ---

# Lambda New (Service Connection)
patch_method("FaceProvider.smali", "lambda$new$2(Ljava/lang/String;)Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;", 
""".method private synthetic lambda$new$2(Ljava/lang/String;)Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;
    .registers 16
    .param p1, "name"  # Ljava/lang/String;
    new-instance v0, Ljava/lang/StringBuilder;
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    sget-object v1, Landroid/hardware/biometrics/face/IFace;->DESCRIPTOR:Ljava/lang/String;
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v0
    const-string v1, "/"
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v0
    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v0
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v1
    invoke-static {v1}, Landroid/hardware/face/FaceSensorConfigurations;->getIFace(Ljava/lang/String;)Landroid/hardware/biometrics/face/IFace;
    move-result-object v2
    const/4 v3, 0x0
    const-string v4, "FaceService"
    if-nez v2, :cond_4e
    new-instance v0, Ljava/lang/StringBuilder;
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    const-string v5, "Unable to get declared service, using fake props: "
    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v0
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v0
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v0
    invoke-static {v4, v0}, Landroid/util/Slog;->e(Ljava/lang/String;Ljava/lang/String;)I
    new-instance v13, Landroid/hardware/biometrics/face/SensorProps;
    invoke-direct {v13}, Landroid/hardware/biometrics/face/SensorProps;-><init>()V
    new-instance v0, Landroid/hardware/biometrics/common/CommonProps;
    invoke-direct {v0}, Landroid/hardware/biometrics/common/CommonProps;-><init>()V
    const/4 v11, 0x1
    iput v11, v0, Landroid/hardware/biometrics/common/CommonProps;->sensorId:I
    iput-object v0, v13, Landroid/hardware/biometrics/face/SensorProps;->commonProps:Landroid/hardware/biometrics/common/CommonProps;
    const/4 v10, 0x1
    new-array v9, v10, [Landroid/hardware/biometrics/face/SensorProps;
    const/4 v10, 0x0
    aput-object v13, v9, v10
    goto :goto_6c
    :cond_4e
    :try_start_4e
    invoke-interface {v2}, Landroid/hardware/biometrics/face/IFace;->getSensorProps()[Landroid/hardware/biometrics/face/SensorProps;
    move-result-object v0
    move-object v9, v0
    :try_end_53
    .catch Landroid/os/RemoteException; {:try_start_4e .. :try_end_53} :catch_54
    goto :goto_6c
    :catch_54
    move-exception v0
    new-instance v5, Ljava/lang/StringBuilder;
    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V
    const-string v6, "Remote exception: "
    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v5
    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v5
    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v5
    invoke-static {v4, v5}, Landroid/util/Slog;->e(Ljava/lang/String;Ljava/lang/String;)I
    return-object v3
    :goto_6c
    :try_start_6c
    new-instance v5, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;
    invoke-virtual {p0}, Lcom/android/server/biometrics/sensors/face/FaceService;->getContext()Landroid/content/Context;
    move-result-object v6
    iget-object v7, p0, Lcom/android/server/biometrics/sensors/face/FaceService;->mBiometricStateCallback:Lcom/android/server/biometrics/sensors/BiometricStateCallback;
    iget-object v8, p0, Lcom/android/server/biometrics/sensors/face/FaceService;->mAuthenticationStateListeners:Lcom/android/server/biometrics/sensors/AuthenticationStateListeners;
    iget-object v11, p0, Lcom/android/server/biometrics/sensors/face/FaceService;->mLockoutResetDispatcher:Lcom/android/server/biometrics/sensors/LockoutResetDispatcher;
    invoke-virtual {p0}, Lcom/android/server/biometrics/sensors/face/FaceService;->getContext()Landroid/content/Context;
    move-result-object v0
    invoke-static {v0}, Lcom/android/server/biometrics/log/BiometricContext;->getInstance(Landroid/content/Context;)Lcom/android/server/biometrics/log/BiometricContext;
    move-result-object v12
    const/4 v13, 0x0
    move-object v10, p1
    invoke-direct/range {v5 .. v13}, Lcom/android/server/biometrics/sensors/face/aidl/FaceProvider;-><init>(Landroid/content/Context;Lcom/android/server/biometrics/sensors/BiometricStateCallback;Lcom/android/server/biometrics/sensors/AuthenticationStateListeners;[Landroid/hardware/biometrics/face/SensorProps;Ljava/lang/String;Lcom/android/server/biometrics/sensors/LockoutResetDispatcher;Lcom/android/server/biometrics/log/BiometricContext;Z)V
    :try_end_85
    .catch Landroid/os/RemoteException; {:try_start_6c .. :try_end_85} :catch_86
    return-object v5
    :catch_86
    move-exception v0
    const-string v5, "Remote exception during init"
    invoke-static {v4, v5}, Landroid/util/Slog;->e(Ljava/lang/String;Ljava/lang/String;)I
    return-object v3
.end method""")

# Cancel Authentication
patch_method("FaceProvider.smali", "cancelAuthentication(ILandroid/os/IBinder;J)V",
""".method public cancelAuthentication(ILandroid/os/IBinder;J)V
    .registers 8
    .param p1, "sensorId"  # I
    .param p2, "token"  # Landroid/os/IBinder;
    .param p3, "requestId"  # J
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_10
    invoke-virtual {v0}, Lax/nd/faceunlock/FaceAuthBridge;->stopAuthenticate()V
    :cond_10
    return-void
.end method""")

# Cancel Enrollment
patch_method("FaceProvider.smali", "cancelEnrollment(ILandroid/os/IBinder;J)V",
""".method public cancelEnrollment(ILandroid/os/IBinder;J)V
    .registers 8
    .param p1, "sensorId"  # I
    .param p2, "token"  # Landroid/os/IBinder;
    .param p3, "requestId"  # J
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_10
    invoke-virtual {v0}, Lax/nd/faceunlock/FaceAuthBridge;->stopEnroll()V
    :cond_10
    return-void
.end method""")

# Get Authenticator ID
patch_method("FaceProvider.smali", "getAuthenticatorId(II)J",
""".method public getAuthenticatorId(II)J
    .registers 7
    .param p1, "sensorId"  # I
    .param p2, "userId"  # I
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_12
    invoke-virtual {v0}, Lax/nd/faceunlock/FaceAuthBridge;->getAuthenticatorId()J
    move-result-wide v0
    return-wide v0
    :cond_12
    const-wide/16 v0, 0x0
    return-wide v0
.end method""")

# Get Enrolled Faces
patch_method("FaceProvider.smali", "getEnrolledFaces(II)Ljava/util/List;",
""".method public getEnrolledFaces(II)Ljava/util/List;
    .registers 7
    .param p1, "sensorId"  # I
    .param p2, "userId"  # I
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(II)",
            "Ljava/util/List<",
            "Landroid/hardware/face/Face;",
            ">;"
        }
    .end annotation
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_12
    invoke-virtual {v0, p1, p2}, Lax/nd/faceunlock/FaceAuthBridge;->getEnrolledFaces(II)Ljava/util/List;
    move-result-object v0
    return-object v0
    :cond_12
    new-instance v0, Ljava/util/ArrayList;
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V
    return-object v0
.end method""")

# Hardware Detection
patch_method("FaceProvider.smali", "isHardwareDetected(I)Z",
""".method public isHardwareDetected(I)Z
    .registers 4
    .param p1, "sensorId"  # I
    const/4 v0, 0x1
    return v0
.end method""")

# Schedule Authenticate
patch_method("FaceProvider.smali", "scheduleAuthenticate(Landroid/os/IBinder;JILcom/android/server/biometrics/sensors/ClientMonitorCallbackConverter;Landroid/hardware/face/FaceAuthenticateOptions;ZIZ)J",
""".method public scheduleAuthenticate(Landroid/os/IBinder;JILcom/android/server/biometrics/sensors/ClientMonitorCallbackConverter;Landroid/hardware/face/FaceAuthenticateOptions;ZIZ)J
    .registers 20
    .param p1, "token"  # Landroid/os/IBinder;
    .param p2, "operationId"  # J
    .param p4, "cookie"  # I
    .param p5, "callback"  # Lcom/android/server/biometrics/sensors/ClientMonitorCallbackConverter;
    .param p6, "options"  # Landroid/hardware/face/FaceAuthenticateOptions;
    .param p7, "restricted"  # Z
    .param p8, "statsClient"  # I
    .param p9, "allowBackgroundAuthentication"  # Z
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_18
    invoke-virtual/range {p6 .. p6}, Landroid/hardware/face/FaceAuthenticateOptions;->getUserId()I
    move-result v1
    invoke-virtual/range {p6 .. p6}, Landroid/hardware/face/FaceAuthenticateOptions;->getSensorId()I
    move-result v2
    invoke-virtual {v0, v2, v1, p5}, Lax/nd/faceunlock/FaceAuthBridge;->startAuthenticate(IILjava/lang/Object;)V
    :cond_18
    const-wide/16 v0, 0x1
    return-wide v0
.end method""")

# Schedule Enroll
patch_method("FaceProvider.smali", "scheduleEnroll(ILandroid/os/IBinder;[BILandroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;[ILandroid/view/Surface;ZLandroid/hardware/face/FaceEnrollOptions;)J",
""".method public scheduleEnroll(ILandroid/os/IBinder;[BILandroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;[ILandroid/view/Surface;ZLandroid/hardware/face/FaceEnrollOptions;)J
    .registers 15
    .param p1, "sensorId"  # I
    .param p2, "token"  # Landroid/os/IBinder;
    .param p3, "hat"  # [B
    .param p4, "userId"  # I
    .param p5, "receiver"  # Landroid/hardware/face/IFaceServiceReceiver;
    .param p6, "opPackageName"  # Ljava/lang/String;
    .param p7, "disabledFeatures"  # [I
    .param p8, "previewSurface"  # Landroid/view/Surface;
    .param p9, "debugConsent"  # Z
    .param p10, "options"  # Landroid/hardware/face/FaceEnrollOptions;
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    invoke-virtual {v0, p4, p5, p8}, Lax/nd/faceunlock/FaceAuthBridge;->startEnroll(ILjava/lang/Object;Landroid/view/Surface;)V
    const-wide/16 v0, 0x1
    return-wide v0
.end method""")

# Generate Challenge
patch_method("FaceProvider.smali", "scheduleGenerateChallenge(IILandroid/os/IBinder;Landroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;)V",
""".method public scheduleGenerateChallenge(IILandroid/os/IBinder;Landroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;)V
    .registers 9
    .param p1, "sensorId"  # I
    .param p2, "userId"  # I
    .param p3, "token"  # Landroid/os/IBinder;
    .param p4, "receiver"  # Landroid/hardware/face/IFaceServiceReceiver;
    .param p5, "opPackageName"  # Ljava/lang/String;
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_10
    invoke-virtual {v0, p1, p2, p4}, Lax/nd/faceunlock/FaceAuthBridge;->generateChallenge(IILjava/lang/Object;)V
    :cond_10
    return-void
.end method""")

# Schedule Remove
patch_method("FaceProvider.smali", "scheduleRemove(ILandroid/os/IBinder;IILandroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;)V",
""".method public scheduleRemove(ILandroid/os/IBinder;IILandroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;)V
    .registers 10
    .param p1, "sensorId"  # I
    .param p2, "token"  # Landroid/os/IBinder;
    .param p3, "faceId"  # I
    .param p4, "userId"  # I
    .param p5, "receiver"  # Landroid/hardware/face/IFaceServiceReceiver;
    .param p6, "opPackageName"  # Ljava/lang/String;
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_10
    invoke-virtual {v0, p4, p3, p5}, Lax/nd/faceunlock/FaceAuthBridge;->remove(IILjava/lang/Object;)V
    :cond_10
    return-void
.end method""")

# Revoke Challenge
patch_method("FaceProvider.smali", "scheduleRevokeChallenge(IILandroid/os/IBinder;Ljava/lang/String;J)V",
""".method public scheduleRevokeChallenge(IILandroid/os/IBinder;Ljava/lang/String;J)V
    .registers 10
    .param p1, "sensorId"  # I
    .param p2, "userId"  # I
    .param p3, "token"  # Landroid/os/IBinder;
    .param p4, "opPackageName"  # Ljava/lang/String;
    .param p5, "challenge"  # J
    invoke-static {}, Lax/nd/faceunlock/FaceAuthBridge;->getInstance()Lax/nd/faceunlock/FaceAuthBridge;
    move-result-object v0
    if-eqz v0, :cond_11
    const/4 v2, 0x0
    invoke-virtual {v0, p1, p2, v2}, Lax/nd/faceunlock/FaceAuthBridge;->revokeChallenge(IILjava/lang/Object;)V
    :cond_11
    return-void
.end method""")

# --- 3. DISABLE SECURE SCREENSHOT ---

patch_method("WindowManagerService.smali", "notifyScreenshotListeners(I)Ljava/util/List;",
""".method public notifyScreenshotListeners(I)Ljava/util/List;
    .locals 1
    invoke-static {}, Ljava/util/Collections;->emptyList()Ljava/util/List;
    move-result-object v0
    return-object v0
.end method""")

patch_method("WindowState.smali", "isSecureLocked()Z",
""".method isSecureLocked()Z
    .locals 1
    const/4 v0, 0x0
    return v0
.end method""")
