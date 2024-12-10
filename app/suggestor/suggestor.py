import joblib
import pandas as pd

from app.suggestor.artifacts.all_tags import all_tags
from app.suggestor.preprocessors import ARTIFACT_PATH, TextPreprocessor


class Suggestor:

    def predict(self, title: str, body: str, threshold: float = 0.25):
        if (title is None or len(title) < 10
                or body is None or len(body) < 10):
            return None
        # Preprocess
        x_preprocessed = TextPreprocessor().preprocess_text(title, body)

        # Predit les Tags
        _path = f"{ARTIFACT_PATH}/model_supervise_proba.pkl"
        model_supervise = joblib.load(_path)
        y_proba = model_supervise.predict_proba(x_preprocessed[0])

        # transformation en DataFrame
        y_proba_df = pd.DataFrame(y_proba, columns=all_tags)
        # Récupération des 5 meilleurs stats
        tags = y_proba_df.iloc[0].sort_values(ascending=False)
        tags = tags.head(5).reset_index().rename(
            columns={'index': 'tag', 0: 'proba'}
        )
        tags.proba = tags.proba.astype(float)
        # Filtre sur le threshold
        tags = tags[tags.proba > threshold].head(5)
        return tags
