.method public scheduleRemove(ILandroid/os/IBinder;IILandroid/hardware/face/IFaceServiceReceiver;Ljava/lang/String;)V
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
.end method