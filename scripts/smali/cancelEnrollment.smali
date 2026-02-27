.method public cancelEnrollment(ILandroid/os/IBinder;J)V
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
.end method