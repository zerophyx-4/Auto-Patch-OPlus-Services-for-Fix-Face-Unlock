.method public static getDeclaredInstances()[Ljava/lang/String;
    .registers 3

    const/4 v0, 0x1

    new-array v0, v0, [Ljava/lang/String;

    const-string v1, "default"

    const/4 v2, 0x0

    aput-object v1, v0, v2

    return-object v0
.end method