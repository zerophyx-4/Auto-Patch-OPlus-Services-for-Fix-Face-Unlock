.method public scheduleGenerateChallenge(IILandroid/os/IBinder;Landroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;)V
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
.end method