{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "7aec1fb7-74c5-4b47-80f6-2e4016dc9b44",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import os "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "60aebb1f-2696-460f-9b1e-086849831290",
   "metadata": {},
   "outputs": [],
   "source": [
    "path = r\"C:\\Users\\eswar\\OneDrive\\Desktop\\Project Folder\\data\\raw\" \n",
    "processed_path = r\"C:\\Users\\eswar\\OneDrive\\Desktop\\Project Folder\\data\\processed\" "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "ca5ee7ce-ade7-4b28-92e5-524fb6784dfa",
   "metadata": {},
   "outputs": [],
   "source": [
    "datasets = {\n",
    "\n",
    "    \"fund_master\": pd.read_csv(os.path.join(path, \"01_fund_master.csv\")),\n",
    "\n",
    "    \"nav_history\": pd.read_csv(os.path.join(path, \"02_nav_history.csv\")),\n",
    "\n",
    "    \"aum_by_fund_house\": pd.read_csv(os.path.join(path, \"03_aum_by_fund_house.csv\")),\n",
    "\n",
    "    \"monthly_sip_inflows\": pd.read_csv(os.path.join(path, \"04_monthly_sip_inflows.csv\")),\n",
    "\n",
    "    \"category_inflows\": pd.read_csv(os.path.join(path, \"05_category_inflows.csv\")),\n",
    "\n",
    "    \"industry_folio_count\": pd.read_csv(os.path.join(path, \"06_industry_folio_count.csv\")),\n",
    "\n",
    "    \"scheme_performance\": pd.read_csv(os.path.join(path, \"07_scheme_performance.csv\")),\n",
    "\n",
    "    \"investor_transactions\": pd.read_csv(os.path.join(path, \"08_investor_transactions.csv\")),\n",
    "\n",
    "    \"portfolio_holdings\": pd.read_csv(os.path.join(path, \"09_portfolio_holdings.csv\")),\n",
    "\n",
    "    \"benchmark_indices\": pd.read_csv(os.path.join(path, \"10_benchmark_indices.csv\")),\n",
    "\n",
    "    \"axis_nav\": pd.read_csv(os.path.join(path, \"axis_nav.csv\")),\n",
    "\n",
    "    \"hdfc_nav\": pd.read_csv(os.path.join(path, \"hdfc_nav.csv\")),\n",
    "\n",
    "    \"icici_nav\": pd.read_csv(os.path.join(path, \"icici_nav.csv\")),\n",
    "\n",
    "    \"kotak_nav\": pd.read_csv(os.path.join(path, \"kotak_nav.csv\")),\n",
    "\n",
    "    \"nippon_nav\": pd.read_csv(os.path.join(path, \"nippon_nav.csv\")),\n",
    "\n",
    "    \"sbi_nav\": pd.read_csv(os.path.join(path, \"sbi_nav.csv\"))\n",
    "\n",
    "} "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "0db67bb9-e0b9-4eb3-9ef0-df71358c748d",
   "metadata": {},
   "outputs": [],
   "source": [
    "date_columns = {\n",
    "    \"fund_master\": [\"launch_date\"],\n",
    "    \"nav_history\": [\"date\"],\n",
    "    \"aum_by_fund_house\": [\"date\"],\n",
    "    \"monthly_sip_inflows\": [\"month\"],\n",
    "    \"category_inflows\": [\"month\"],\n",
    "    \"industry_folio_count\": [\"month\"],\n",
    "    \"investor_transactions\": [\"transaction_date\"],\n",
    "    \"benchmark_indices\": [\"date\"],\n",
    "    \"portfolio_holdings\": [\"portfolio_date\"]\n",
    "}\n",
    "\n",
    "for df_name, cols in date_columns.items():\n",
    "    for col in cols:\n",
    "        datasets[df_name][col] = pd.to_datetime(\n",
    "            datasets[df_name][col],\n",
    "            errors=\"coerce\"\n",
    "        ) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "77c29541-c704-449b-9c96-34b67b906b16",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# clean nav_history.csv\n",
    "# sort\n",
    "nav = datasets[\"nav_history\"]\n",
    "\n",
    "nav = nav.sort_values(\n",
    "    [\"amfi_code\",\"date\"]\n",
    ") \n",
    "\n",
    "# remove duplicates \n",
    "nav = nav.drop_duplicates(\n",
    "    subset=[\"amfi_code\",\"date\"]\n",
    ")\n",
    "\n",
    "#  check missing nav\n",
    "nav.isnull().sum()\n",
    "\n",
    "# verify duplicate values \n",
    "nav.duplicated(subset=[\"amfi_code\", \"date\"]).sum()\n",
    "\n",
    "# verify invalid NAV values \n",
    "(nav[\"nav\"] <= 0).sum() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "b9fe8d15-0d35-4853-a633-334563594157",
   "metadata": {},
   "outputs": [],
   "source": [
    "nav.to_csv(os.path.join(processed_path, \"02_nav_history.csv\"), index=False) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "c54e4294-0d02-4a9e-a0f8-062aaca77508",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# cleaning investor_transactions\n",
    "transactions = datasets[\"investor_transactions\"].copy() \n",
    "\n",
    "# Convert transaction date\n",
    "transactions[\"transaction_date\"] = pd.to_datetime(\n",
    "    transactions[\"transaction_date\"],\n",
    "    errors=\"coerce\"\n",
    ") \n",
    "transactions[\"transaction_date\"].isnull().sum() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "e5911ebb-87f5-4088-baf6-ffd74cd68ae9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "transaction_type\n",
       "SIP           19716\n",
       "Lumpsum        8095\n",
       "Redemption     4967\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#check transdaction types\n",
    "transactions[\"transaction_type\"].value_counts()  "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "e590ed78-2dd4-4104-9088-3e81bef61ccc",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Validate amount\n",
    "(transactions[\"amount_inr\"] <= 0).sum() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "d9bd3d89-1171-404a-9adf-1cd8db29823c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Check date conversion\n",
    "transactions[\"transaction_date\"] = pd.to_datetime(\n",
    "    transactions[\"transaction_date\"],\n",
    "    errors=\"coerce\"\n",
    ") \n",
    "transactions[\"transaction_date\"].isnull().sum() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "33f6bdff-505d-4c45-ad6e-c3c3b1b6035c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "kyc_status\n",
       "Verified    30146\n",
       "Pending      2632\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#check KYC status \n",
    "transactions[\"kyc_status\"].value_counts() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "009cde29-10cc-42c4-a7ba-b2cb623bcbdc",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Check Amount Validation \n",
    "(transactions[\"amount_inr\"] <= 0).sum() \n",
    "\n",
    "# check Duplicate Rows \n",
    "transactions.duplicated().sum() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "9e5d0139-4d89-40e4-9da9-88b79b4d06e4",
   "metadata": {},
   "outputs": [],
   "source": [
    "transactions.to_csv(\n",
    "    os.path.join(processed_path, \"08_investor_transactions.csv\"),\n",
    "    index=False\n",
    ")  "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "b3f832e6-be68-43dc-a2cf-998cf66b7738",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Anomalies in return_1yr_pct: 0\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>scheme_name</th>\n",
       "      <th>return_1yr_pct</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [scheme_name, return_1yr_pct]\n",
       "Index: []"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Anomalies in return_3yr_pct: 0\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>scheme_name</th>\n",
       "      <th>return_3yr_pct</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [scheme_name, return_3yr_pct]\n",
       "Index: []"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Anomalies in return_5yr_pct: 0\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>scheme_name</th>\n",
       "      <th>return_5yr_pct</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [scheme_name, return_5yr_pct]\n",
       "Index: []"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Anomalies in benchmark_3yr_pct: 0\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>scheme_name</th>\n",
       "      <th>benchmark_3yr_pct</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [scheme_name, benchmark_3yr_pct]\n",
       "Index: []"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# clean scheme_performance\n",
    "performance = datasets[\"scheme_performance\"].copy() \n",
    "\n",
    "#check data types\n",
    "performance.dtypes \n",
    "\n",
    "#check missing values in return columns \n",
    "return_cols = [\n",
    "    \"return_1yr_pct\",\n",
    "    \"return_3yr_pct\",\n",
    "    \"return_5yr_pct\",\n",
    "    \"benchmark_3yr_pct\"\n",
    "]\n",
    "\n",
    "performance[return_cols].isnull().sum() \n",
    "\n",
    "#Flag anomalous return values\n",
    "for col in return_cols:\n",
    "    anomalies = performance[\n",
    "        (performance[col] < -100) |\n",
    "        (performance[col] > 100)\n",
    "    ]\n",
    "\n",
    "    print(f\"\\nAnomalies in {col}: {len(anomalies)}\")\n",
    "    display(anomalies[[\"scheme_name\", col]])\n",
    "\n",
    "\n",
    "#Validate expense ratio\n",
    "performance[\n",
    "    (performance[\"expense_ratio_pct\"] < 0.1) |\n",
    "    (performance[\"expense_ratio_pct\"] > 2.5)\n",
    "] \n",
    "\n",
    "\n",
    "# check duplicates \n",
    "performance.duplicated().sum() \n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "4c794140-9a26-46af-8fcc-3bcba1f2d93e",
   "metadata": {},
   "outputs": [],
   "source": [
    "performance.to_csv(\n",
    "    os.path.join(processed_path, \"07_scheme_performance.csv\"),\n",
    "    index=False\n",
    ") "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
