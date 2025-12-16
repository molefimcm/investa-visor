
// MVP: Compute stock/bond/cash allocation based on risk appetite

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

// risk_level: 0=conservative, 1=balanced, 2=aggressive
// outputs: stocks_pct, bonds_pct, cash_pct (0..100)
EXPORT void allocation(int risk_level, int *stocks_pct, int *bonds_pct, int *cash_pct)
{
    if (!stocks_pct || !bonds_pct || !cash_pct) return;

    switch (risk_level)
    {
        case 0: // conservative
            *stocks_pct = 30; *bonds_pct = 60; *cash_pct = 10;
            break;
        case 2: // aggressive
            *stocks_pct = 80; *bonds_pct = 15; *cash_pct = 5;
            break;
        default: // balanced
            *stocks_pct = 60; *bonds_pct = 35; *cash_pct = 5;
            break;
    }
}
