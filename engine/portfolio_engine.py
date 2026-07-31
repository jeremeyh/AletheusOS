import pandas as pd


def numeric_sum(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df.columns:
        return 0.0
    return float(pd.to_numeric(df[col], errors="coerce").fillna(0).sum())


def get_asset_snapshot(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "portfolio_value": 0.0,
            "purchase_basis": 0.0,
            "asset_count": 0,
            "cards": 0,
            "memorabilia": 0,
            "pops": 0,
            "bobbleheads": 0,
            "change_30": 0.0,
            "change_pct": 0.0,
            "roi": 0.0,
        }

    portfolio_value = numeric_sum(df, "current_value")
    purchase_basis = numeric_sum(df, "purchase_price")
    gain = portfolio_value - purchase_basis
    roi = (gain / purchase_basis * 100) if purchase_basis else 0.0

    category_series = (
        df["category"].fillna("").str.lower()
        if "category" in df.columns
        else pd.Series([])
    )
    cards = (
        int(category_series.str.contains("card").sum())
        if not category_series.empty
        else 0
    )
    memorabilia = (
        int(category_series.str.contains("memorabilia").sum())
        if not category_series.empty
        else 0
    )
    pops = (
        int(category_series.str.contains("funko|pop").sum())
        if not category_series.empty
        else 0
    )
    bobbleheads = (
        int(category_series.str.contains("bobble").sum())
        if not category_series.empty
        else 0
    )

    return {
        "portfolio_value": portfolio_value,
        "purchase_basis": purchase_basis,
        "asset_count": len(df),
        "cards": cards,
        "memorabilia": memorabilia,
        "pops": pops,
        "bobbleheads": bobbleheads,
        "change_30": gain,
        "change_pct": roi,
        "roi": roi,
    }


def allocation_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if df.empty or column not in df.columns:
        return pd.DataFrame(columns=[column, "count", "value"])
    temp = df.copy()
    temp["current_value"] = pd.to_numeric(
        temp["current_value"], errors="coerce"
    ).fillna(0)
    grouped = (
        temp.groupby(column, dropna=False)
        .agg(count=("id", "count"), value=("current_value", "sum"))
        .reset_index()
    )
    grouped[column] = grouped[column].replace("", "Unassigned").fillna("Unassigned")
    return grouped.sort_values("value", ascending=False)
