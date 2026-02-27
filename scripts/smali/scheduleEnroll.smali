.method public scheduleEnroll(ILandroid/os/IBinder;[BILandroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;[ILandroid/view/Surface;ZLandroid/hardware/face/FaceEnrollOptions;)J
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
.end method