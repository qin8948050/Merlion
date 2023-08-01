def init_model():
    # Import models & configs
    from merlion.models.anomaly.forecast_based.arima import Arima, ArimaConfig
    from merlion.models.anomaly.forecast_based.ets import ETS, ETSConfig
    from merlion.models.anomaly.forecast_based.prophet import ProphetDetector, ProphetDetectorConfig

    # Import a post-rule for thresholding
    from merlion.post_process.threshold import AggregateAlarms

    # Import a data processing transform
    from merlion.transform.moving_average import DifferenceTransform

    # All models are initialized using the syntax ModelClass(config), where config
    # is a model-specific configuration object. This is where you specify any
    # algorithm-specific hyperparameters, any data pre-processing transforms, and
    # the post-rule you want to use to post-process the anomaly scores (to reduce
    # noisiness when firing alerts).

    # We initialize isolation forest using the default config
    config1 = ArimaConfig()
    model1 = Arima(config1)

    # We use a WindStats model that splits each week into windows of 60 minutes
    # each. Anomaly scores in Merlion correspond to z-scores. By default, we would
    # like to fire an alert for any 4-sigma event, so we specify a threshold rule
    # which achieves this.
    config2 = ETSConfig()
    model2 = ETS(config2)

    # Prophet is a popular forecasting algorithm. Here, we specify that we would like
    # to pre-processes the input time series by applying a difference transform,
    # before running the model on it.
    config3 = ProphetDetectorConfig(transform=DifferenceTransform())
    model3 = ProphetDetector(config3)

    from merlion.models.ensemble.anomaly import DetectorEnsemble, DetectorEnsembleConfig

    ensemble_config = DetectorEnsembleConfig(threshold=AggregateAlarms(alm_threshold=4))
    ensemble = DetectorEnsemble(config=ensemble_config, models=[model1, model2, model3])
    return model1, model2, model3, ensemble

def model_infer(model1,test_data):
    # Here is a full example for the first model, IsolationForest
    scores_1 = model1.get_anomaly_score(test_data)
    scores_1_df = scores_1.to_pd()
    print(f"{type(model1).__name__}.get_anomaly_score() nonzero values (raw)")
    print(scores_1_df[scores_1_df.iloc[:, 0] != 0])
    print()

    labels_1 = model1.get_anomaly_label(test_data)
    labels_1_df = labels_1.to_pd()
    print(f"{type(model1).__name__}.get_anomaly_label() nonzero values (post-processed)")
    print(labels_1_df[labels_1_df.iloc[:, 0] != 0])
    print()

    print(f"{type(model1).__name__} fires {(labels_1_df.values != 0).sum()} alarms")
    print()

    print("Raw scores at the locations where alarms were fired:")
    print(scores_1_df[labels_1_df.iloc[:, 0] != 0])
    print("Post-processed scores are interpretable as z-scores")
    print("Raw scores are challenging to interpret")
    print("######################################")
    return scores_1,labels_1

def qa_evalution(models:[tuple],test_labels,):
    from merlion.evaluate.anomaly import TSADMetric

    for model, labels in models:
        print(f"{type(model).__name__}")
        precision = TSADMetric.Precision.value(ground_truth=test_labels, predict=labels)
        recall = TSADMetric.Recall.value(ground_truth=test_labels, predict=labels)
        f1 = TSADMetric.F1.value(ground_truth=test_labels, predict=labels)
        mttd = TSADMetric.MeanTimeToDetect.value(ground_truth=test_labels, predict=labels)
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1:        {f1:.4f}")
        print(f"MTTD:      {mttd}")
        print()

