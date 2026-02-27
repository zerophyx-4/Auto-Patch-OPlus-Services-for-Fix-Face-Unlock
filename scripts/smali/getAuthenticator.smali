.method public getAuthenticatorId(II)J
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
.end method