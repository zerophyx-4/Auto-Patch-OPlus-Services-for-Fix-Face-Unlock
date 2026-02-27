.method public scheduleAuthenticate(Landroid/os/IBinder;JILcom/android/server/biometrics/sensors/ClientMonitorCallbackConverter;Landroid/hardware/face/FaceAuthenticateOptions;ZIZ)J
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
.end method