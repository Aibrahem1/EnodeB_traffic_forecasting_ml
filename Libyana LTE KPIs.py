#importing essential Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Setting the pd configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100)
# **** importing Libyana LTE KPI Data
LTEKPIS_raw = pd.read_excel('Datasets/Libyana Dataset JUN25/History Query-LTE KPI one year daily.xlsx',
                        sheet_name='Sheet0')
#Exploratory DATA Analysis
LTEKPIS_raw.head(10)
LTEKPIS_raw.shape #(61647 x 95)
LTEKPIS_raw.columns # some columns require to be renamed for clarity

##### ***** Select KEY Radio Features required for forecasting (technical discussion as to why will be convered)
LTEKPIS_clean = LTEKPIS_raw[[
    #Time Stamp
    'Begin Time',
    'Granularity',
    #BTS and Cells identifiers
    'eNodeB ID',
    'eNodeB Name',
    'E-UTRAN FDD Cell ID',
    'E-UTRAN FDD Cell Name',
    # Target variables (choose one for Y)
    'PS Traffic Volume(GB)_ITBBU&SDR',
    'DL E-UTRAN IP Throughput(Mbps)_ITBBU&SDR',
    'Cell DL Average Aggregated Throughput(Mbps)',
    'DL PRB Utilization Rate(%)',
    # Load & Resource KPIs
    'UL PRB Utilization Rate(%)',
    'DL PRB Available (Bandwidth)',
    'Mean Number of RRC Connection User',
    'Maximum Active User Number on User Plane',
    'Maximum Number of RRC Connection User',
    # Quality KPIs
    'RRC Establishment Success Rate(%)',
    'E-RAB Setup Success Rate(%)',
    'E-RAB Drop Rate(%)',
    'RRC Drop Rate(%)',
    'Cell Uplink BLER(%)',
    'Cell Downlink BLER(%)',
    # RF/PHY Layer
    'DL Average MCS',
    'UL Average MCS',
    'Average CQI(N/A)',
    'Ratio of CQI>7 Percentage',
    'Ratio of CQI >= 10 (64QAM)',
    # Coverage and Interference
    'LTE Average TA(km)',
    'Average Cell RSSI(dBm)',
    'Ratio of SINR<-3dB',
    'Ratio of RSRP in Range of  [-110,-106]dBm',
    'Ratio of RSRP in Range of  [-115,-111]dBm',
    'Ratio of RSRP in Range of  [-120,-116]dBm',
    'Ratio of RSRP in Range of  [-140,-121]dBm',
    # Mobility
    'Success Rate of Outgoing Handover(Cell)(%)',
    'Success Rate of Intra-RAT Inter-frequency Cell Outgoing Handover(%)',
    'Number of Ping-Pong Handover']].rename(columns={
    # Time Stamp
    'Begin Time': 'timestamp',
    'Granularity': 'granularity',
    # BTS and Cell Identifiers
    'eNodeB ID': 'enodeb_id',
    'eNodeB Name': 'enodeb_name',
    'E-UTRAN FDD Cell ID': 'cell_id',
    'E-UTRAN FDD Cell Name': 'cell_name',
    # Target Variables
    'PS Traffic Volume(GB)_ITBBU&SDR': 'ps_traffic_volume_gb',
    'DL E-UTRAN IP Throughput(Mbps)_ITBBU&SDR': 'dl_throughput_mbps',
    'Cell DL Average Aggregated Throughput(Mbps)': 'cell_dl_avg_agg_throughput',
    'DL PRB Utilization Rate(%)': 'dl_prb_util_%',
    # Load & Resource KPIs
    'UL PRB Utilization Rate(%)': 'ul_prb_util_%',
    'DL PRB Available (Bandwidth)': 'dl_prb_available_bandwidth',
    'Mean Number of RRC Connection User': 'mean_no_rrc_users',
    'Maximum Active User Number on User Plane': 'max_active_no_users_uplane',
    'Maximum Number of RRC Connection User': 'max_no_rrc_users',
    # Quality KPIs
    'RRC Establishment Success Rate(%)': 'rrc_success_rate_%',
    'E-RAB Setup Success Rate(%)': 'erab_setup_success_rate_%',
    'E-RAB Drop Rate(%)': 'erab_drop_rate_%',
    'RRC Drop Rate(%)': 'rrc_drop_rate_%',
    'Cell Uplink BLER(%)': 'cell_ul_bler_rate_%',
    'Cell Downlink BLER(%)': 'cell_dl_bler_rate_%',
    # RF/PHY Layer
    'DL Average MCS': 'dl_avg_mcs',
    'UL Average MCS': 'ul_avg_mcs',
    'Average CQI(N/A)': 'avg_cqi',
    'Ratio of CQI>7 Percentage': 'ratio_cqi_gt7',
    'Ratio of CQI >= 10 (64QAM)': 'ratio_cqi_gte10',
    # Coverage and Interference
    'LTE Average TA(km)': 'avg_ta_km',
    'Average Cell RSSI(dBm)': 'avg_rssi_dbm',
    'Ratio of SINR<-3dB': 'ratio_sinr_lt_neg3',
    'Ratio of RSRP in Range of  [-110,-106]dBm': 'rsrp_range_110_106_Ratio_%',
    'Ratio of RSRP in Range of  [-115,-111]dBm': 'rsrp_range_115_111_Ratio_%',
    'Ratio of RSRP in Range of  [-120,-116]dBm': 'rsrp_range_120_116_Ratio_%',
    'Ratio of RSRP in Range of  [-140,-121]dBm': 'rsrp_range_140_121_Ratio_%',
    # Mobility
    'Success Rate of Outgoing Handover(Cell)(%)': 'outgoing_ho_success_rate_%',
    'Success Rate of Intra-RAT Inter-frequency Cell Outgoing Handover(%)': 'intra_rat_ho_success_rate_%',
    'Number of Ping-Pong Handover': 'no_ping_pong_ho_count'
})

## == Exporting Data to local disk
LTEKPIS_clean.to_csv('exports/Libyana LTE KPIs/LTEKPIS_clean.csv')

## == Exploratory Data analysis of the cleaned data
LTEKPIS_clean.columns
LTEKPIS_clean['enodeb_name'].nunique() # A total of 16 eNodeBs are in the dataset
LTEKPIS_clean['cell_name'].nunique()   # A total of 168 cells are in the dataset
LTEKPIS_clean.shape #Data contains (61647 x 35)
LTEKPIS_clean.dtypes # timestamp is not in the correct formate, therefore, it needs to be changed to date format
# ***** dropping enodeb_id (removing redundancies)
LTEKPIS_clean.drop(columns='enodeb_id', inplace=True) #unwanted redundant

## == modify the data type for timestamp feature
LTEKPIS_clean['timestamp'] = pd.to_datetime(LTEKPIS_clean['timestamp'])

LTEKPIS_clean.shape # to confirm that the data structure hasn't changed
LTEKPIS_clean.dtypes # data type of time stamp has successfully been changed
#Writting data to local disk 'overwritting existing one'
LTEKPIS_clean.to_csv('exports/Libyana LTE KPIs/LTEKPIS_clean.csv')

## subsetting
LTEKPIS_clean[LTEKPIS_clean['timestamp'].between('2024-12-24', '2024-12-25')] #testing
#subsetting 1
LTEKPIS_clean[np.logical_and(
    LTEKPIS_clean['timestamp'].between('2024-12-24', '2024-12-25'),
    LTEKPIS_clean['enodeb_name']=='TRI055L'
)]
# subsetting 2 (best-most common)
LTEKPIS_clean[(LTEKPIS_clean['enodeb_name'] == 'TRI055L') &
              (LTEKPIS_clean['timestamp'].between('2024-12-24', '2025-01-25')) &
              (LTEKPIS_clean['cell_id']==1)]

#### ===== Descriptive Statistics summary
import pandas as pd
#Descriptive Statistics for Numerical variables
LTEKPIS_clean_numeric_data = LTEKPIS_clean.select_dtypes(include='number')

LTEKPIS_clean_numeric_data.dtypes

summary_statistics = pd.DataFrame({
    'Min': LTEKPIS_clean_numeric_data.min(),
    'Max': LTEKPIS_clean_numeric_data.max(),
    'Mean': LTEKPIS_clean_numeric_data.mean(),
    'Std. Deviation': LTEKPIS_clean_numeric_data.std(),
    'Variance': LTEKPIS_clean_numeric_data.var(),
    'Skewness': LTEKPIS_clean_numeric_data.skew(),
    'Kurtosis': LTEKPIS_clean_numeric_data.kurtosis(),
    'Sum': LTEKPIS_clean_numeric_data.sum(),
    'Median': LTEKPIS_clean_numeric_data.median(),
    'Missing': LTEKPIS_clean_numeric_data.isna().sum(),
    'Row count': len(LTEKPIS_clean_numeric_data)})

# Rename index to 'Column' and convert it into a column in the DataFrame
summary_statistics.index.name = 'Feature'
summary_statistics.reset_index(inplace=True)
#Exporting the Statitics to local Disk
summary_statistics
summary_statistics.to_excel("exports/Libyana LTE KPIs/summary_statistics_python.xlsx", index=False)

# Descriptive statistics for categorical variables
LTEKPIS_clean.dtypes

LTEKPIS_clean['enodeb_name'].unique()
LTEKPIS_clean['enodeb_id'].nunique()
LTEKPIS_clean['enodeb_name'].value_counts()


## === Correlation Analysis
#Computes Pearson correlation (linear relationship) Range: [-1, 1]
corr_LTEKPI_clean_numeric = LTEKPIS_clean_numeric_data.corr(method='pearson')
#Writting Correlation Matrix to disk
corr_LTEKPI_clean_numeric.to_excel('exports/Libyana LTE KPIs/corr_LTEKPI_clean_numeric.xlsx', index=True)
## Correlation Visualisation
import matplotlib.pyplot as plt
import seaborn as sns
# Plotting correlation heatmap
plt.figure(figsize=(35,25))
sns.heatmap(corr_LTEKPI_clean_numeric,
            annot=True,                 # Display correlation values inside the heatmap cells
            fmt='.2f',                  # Format the numbers to 2 decimal places
            cmap='coolwarm',            # Diverging color palette from blue to red
            square=True,                # Shrink the color bar to make space for plot
            cbar_kws={'shrink': 0.5},   # Forcing perfect square for visual asthetics
            annot_kws={'fontsize': 6}  # <-- reducing font size inside the boxed for clarity
            )
plt.title('Pair-wise Correlation Matrix of LTE KPIs') # Set plot title
plt.xticks(rotation= 45, fontsize = 8, ha='right')    # Rotate and align x-axis tick labels
plt.xlabel('KPI Features')
plt.yticks(fontsize = 8)
plt.ylabel('KPI Features')
plt.tight_layout()                                    # Auto-adjust layout to prevent overlap
plt.show(block= True)

# ===== Time Series Plots (To visually inspect the data for patterns, trends, seasonality, and anomalies)
# Plotting relationship for TRI055
LTEKPIS_clean['cell_name'].unique()
(LTEKPIS_clean[LTEKPIS_clean['enodeb_name']=='TRI055L-1'].plot(kind='scatter',
                                                            x ='timestamp',
                                                            y ='ps_traffic_volume_gb'))
plt.show(block=True)




# ==== plots
# Step 2: Add Year and Month for grouping
import pandas as pd
import matplotlib.pyplot as plt

LTEKPIS_clean['Year'] = LTEKPIS_clean['timestamp'].dt.year
LTEKPIS_clean['Month'] = LTEKPIS_clean['timestamp'].dt.month_name().str[:3]  # e.g., 'Jan', 'Feb'
LTEKPIS_clean['Month_Num'] = LTEKPIS_clean['timestamp'].dt.month  # for sorting

LTEKPIS_clean

# Step 3: Group by enodeb_name + Year + Month and compute mean
monthly_avg = (
    LTEKPIS_clean.groupby(['enodeb_name', 'Year', 'Month_Num','Month'])
    ['ps_traffic_volume_gb']
    .mean()
    .reset_index()
)

# Step 4: Create 'Period' column for x-axis
monthly_avg['Period'] = monthly_avg['Year'].astype(str) + '-' + monthly_avg['Month']
monthly_avg.sort_values(by=['Year', 'Month_Num'], inplace=True)

# Step 5: Plot for each enodeb_name
plt.figure(figsize=(14, 7))

for name, group in monthly_avg.groupby('enodeb_name'):
    plt.plot(group['Period'], group['ps_traffic_volume_gb'], label=name, marker='o')

plt.xticks(rotation=45, ha='right')
plt.title('Monthly Average PS Traffic Volume per eNodeB')
plt.xlabel('Period')
plt.ylabel('Avg PS Traffic Volume (GB)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show(block=True)


# **** Per Cell

# Group by cell_name + Year + Month and compute mean
monthly_avg_cell_name = (
    LTEKPIS_clean.groupby(['cell_name', 'Year', 'Month_Num','Month'])
    ['ps_traffic_volume_gb']
    .mean()
    .reset_index()
)

# Step 4: Create 'Period' column for x-axis
monthly_avg_cell_name['Period'] = monthly_avg['Year'].astype(str) + '-' + monthly_avg['Month']
monthly_avg_cell_name.sort_values(by=['Year', 'Month_Num'], inplace=True)

monthly_avg_cell_name.dropna(inplace=True)

monthly_avg_cell_name['cell_name'].nunique()
LTEKPIS_clean['cell_name']. nunique()

# Step 5: Plot for each enodeb_name
plt.figure(figsize=(14, 7))

for name, group in monthly_avg_cell_name.groupby('cell_name'):
    plt.plot(group['Period'], group['ps_traffic_volume_gb'], label=name, marker='o')

plt.xticks(rotation=45, ha='right')
plt.title('Monthly Average PS Traffic Volume per eNodeB')
plt.xlabel('Period')
plt.ylabel('Avg PS Traffic Volume (GB)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show(block=True)