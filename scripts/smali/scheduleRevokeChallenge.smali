.method public scheduleRevokeChallenge(IILandroid/os/IBinder;Ljava/lang/String;J)V
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
.end method