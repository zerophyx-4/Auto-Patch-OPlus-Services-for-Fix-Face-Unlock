.method public isHardwareDetected(I)Z
    .registers 4
    .param p1, "sensorId"  # I

    const/4 v0, 0x1

    return v0
.end method