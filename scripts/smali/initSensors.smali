.method private initSensors(Z[Landroid/hardware/biometrics/face/SensorProps;)V
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
.end method