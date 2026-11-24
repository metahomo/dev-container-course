"""작은 ML 모델을 몇 초 안에 학습해서 파일로 저장해요.

데이터: 붓꽃(Iris) 150건 — R. A. Fisher, UCI Machine Learning Repository, CC BY 4.0
모델: scikit-learn 로지스틱 회귀 (BSD-3-Clause)

실행:  uv run --no-project --with scikit-learn==1.9.1 python train.py
"""
import json
import sys
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train(out_dir: Path) -> dict:
    """학습하고 out_dir/model.joblib 과 out_dir/metrics.json 을 만든 뒤 지표를 돌려줘요."""
    out_dir.mkdir(parents=True, exist_ok=True)
    data = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42, stratify=data.target
    )
    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)
    metrics = {
        "accuracy": round(float(model.score(x_test, y_test)), 4),
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
    }
    # 모델과 함께 "이 모델이 아는 정보"(클래스 이름·특징 이름)를 같이 저장해요.
    joblib.dump(
        {
            "model": model,
            "target_names": [str(n) for n in data.target_names],
            "feature_names": list(data.feature_names),
        },
        out_dir / "model.joblib",
    )
    (out_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2))
    return metrics


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "model")
    print(train(out))
    print(f"저장했어요: {out / 'model.joblib'}")
