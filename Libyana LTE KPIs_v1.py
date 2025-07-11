# **** importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
from IPython.core.pylabtools import figsize
from IPython.display import display


#pip install xlsxwriter
#pip install IPython

# ==============================================================================
#  CONFIGURATION AND SETUP
# ==============================================================================
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
#-------------------------------------------------------------------------------

# ==============================================================================
# DATA IMPORT
# ==============================================================================
## 📁 importing Libyana LTE KPI Data
lte_rawdata = pd.read_excel('Datasets/Libyana Dataset JUN25/History Query-LTE KPI one year daily.xlsx',
                            sheet_name='Sheet0')

## ==============================================================================
# ⚙️️ EDA summary function with Export feature
## ==============================================================================
def basic_EDA_summary(df, name="DataFrame"):
    print(f"\n ---- Head of {name}")
    display(df.head(10))
    print(f"\n ---- Shape of {name} dataframe")
    display(df.shape)
    print(f"\n ---- Data Types of {name}")
    display(df.dtypes)
    print(f"\n ---- Info of {name}")
    display(df.info())
    # Format export file path dynamically
    file_path = f"exports/Libyana LTE KPIs/{name}_eda_summary.xlsx"
    # Export sections to Excel sheets
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.head(10).to_excel(writer, sheet_name="Head", index=False)
        pd.DataFrame({
            'Rows': [df.shape[0]],
            'Columns': [df.shape[1]]
        }).to_excel(writer, sheet_name="Shape", index=False)
        df.dtypes.reset_index().rename(columns={0: 'DataType', 'index': 'Column'}) \
            .to_excel(writer, sheet_name="DataTypes", index=False)
    print(f"\n✅ Exported EDA summary to {file_path}")

# ==============================================================================
# 🔍 Exploring lte raw data
## ==============================================================================
basic_EDA_summary(lte_rawdata, name="LTE Raw Data")

# 🔍 checking how many LTE enodeB
lte_rawdata['eNodeB Name'].unique()
lte_rawdata['eNodeB Name'].nunique()
lte_rawdata['eNodeB Name'].value_counts()
# 🔍 checking how many LTE Cells
lte_rawdata['E-UTRAN FDD Cell Name'].unique()
lte_rawdata['E-UTRAN FDD Cell Name'].nunique()
lte_rawdata['E-UTRAN FDD Cell Name'].value_counts().to_csv('exports/noofcellsobsercations.csv')

# ==============================================================================
# 📊 Select KEY Radio Features required for forecasting PS traffic
# ==============================================================================
lte_ps_traffic = lte_rawdata[[
    #Time Stamp
    'Begin Time',
    #BTS and Cells identifiers
    'eNodeB Name',
    'E-UTRAN FDD Cell Name',
    # Target variables (choose one for Y)
    'PS Traffic Volume(GB)_ITBBU&SDR',
    # Key traffic load indicators
    'UL PRB Utilization Rate(%)',
    'DL PRB Available (Bandwidth)',
    'Mean Number of RRC Connection User',
    'Maximum Active User Number on User Plane',
    # Quality KPIs
    'RRC Establishment Success Rate(%)',
    'E-RAB Setup Success Rate(%)',
    'E-RAB Drop Rate(%)',
    'RRC Drop Rate(%)',
    'Cell Uplink BLER(%)',
    'Cell Downlink BLER(%)',
    # Signal quality affecting throughput
    'DL Average MCS',
    'UL Average MCS',
    'Average CQI(N/A)',
    # Coverage and Interference
    'LTE Average TA(km)',
    'Average Cell RSSI(dBm)',
    # Mobility
    'Success Rate of Outgoing Handover(Cell)(%)',
    'Success Rate of Intra-RAT Inter-frequency Cell Outgoing Handover(%)',
    'Number of Ping-Pong Handover']].rename(columns={
    # Time Stamp
    'Begin Time': 'timestamp',
    # Target Variables
    'PS Traffic Volume(GB)_ITBBU&SDR': 'ps_traffic_volume_gb',
    # BTS and Cell Identifiers
    'eNodeB Name': 'enodeb_name',
    'E-UTRAN FDD Cell Name': 'cell_name',
    # Key traffic load indicators
    'UL PRB Utilization Rate(%)': 'ul_prb_util_%',
    'DL PRB Available (Bandwidth)': 'dl_prb_available_bandwidth',
    'Mean Number of RRC Connection User': 'mean_no_rrc_users',
    'Maximum Active User Number on User Plane': 'max_active_no_users_uplane',
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
    'Average CQI(N/A)' : 'avg_cqi',
    # Coverage and Interference
    'LTE Average TA(km)': 'avg_ta_km',
    'Average Cell RSSI(dBm)': 'avg_rssi_dbm',
    # Mobility
    'Success Rate of Outgoing Handover(Cell)(%)': 'outgoing_ho_success_rate_%',
    'Success Rate of Intra-RAT Inter-frequency Cell Outgoing Handover(%)': 'intra_rat_ho_success_rate_%',
    'Number of Ping-Pong Handover': 'no_ping_pong_ho_count'
})
# ==============================================================================
# 🔍  Exploring lte_ps_traffic EDA Summary
# ==============================================================================
basic_EDA_summary(lte_ps_traffic, name = 'lte ps traffic')

# 🔍 checking how many LTE enodeB
lte_rawdata['enodeb_name'].unique()
lte_rawdata['enodeb_name'].nunique()
lte_rawdata['enodeb_name'].value_counts()
# 🔍 checking how many LTE Cells
lte_rawdata['cell_name'].unique()
lte_rawdata['cell_name'].nunique()
lte_rawdata['cell_name'].value_counts().to_csv('exports/ltepstraffi_countofcells.csv')


# ==============================================================================
# ⚙️️ Summary statistics Function: Computes descriptive statistics for all numeric columns and exports to Excel
# ==============================================================================
def descriptive_statistics_numeric(df, name="DataFrame"):
    numeric_df = df.select_dtypes(include='number')
    summary_stats = pd.DataFrame({
        'Min': numeric_df.min().round(2),
        'Max': numeric_df.max().round(2),
        'Mean': numeric_df.mean().round(2),
        'Std. Deviation': numeric_df.std().round(2),
        'Variance': numeric_df.var().round(2),
        'Skewness': numeric_df.skew().round(2),
        'Kurtosis': numeric_df.kurtosis().round(2),
        'Sum': numeric_df.sum().round(2).round(2),
        'Median': numeric_df.median().round(2),
        'Missing': numeric_df.isna().sum().round(2),
        'Row count': len(numeric_df)
    })
    summary_stats.index.name = 'Feature'
    summary_stats.reset_index(inplace=True)
    file_path = "exports/Libyana LTE KPIs/" + name + "_numeric_summary.xlsx"
    summary_stats.to_excel(file_path, index=False)
    print("\n🟢 Exported numeric summary for '" + name + "' to: " + file_path)
    return summary_stats

# ==============================================================================
# 🔍 conduct Descriptive analysis for lte_ps_traffic
# ==============================================================================
descriptive_statistics_numeric(lte_ps_traffic, name ='lte_ps_traffic')

# ==============================================================================
#  Group by timestamp and enodeb_name, and aggregate using appropriate functions
# ==============================================================================
agg_sites_traffic = lte_ps_traffic.groupby(['timestamp', 'enodeb_name']).agg({
    'ps_traffic_volume_gb': 'sum',
    'ul_prb_util_%': 'mean',
    'dl_prb_available_bandwidth': 'mean',
    'mean_no_rrc_users': 'sum',
    'max_active_no_users_uplane': 'sum',
    'rrc_success_rate_%': 'mean',
    'erab_setup_success_rate_%': 'mean',
    'erab_drop_rate_%': 'mean',
    'rrc_drop_rate_%': 'mean',
    'cell_ul_bler_rate_%': 'mean',
    'cell_dl_bler_rate_%': 'mean',
    'dl_avg_mcs': 'mean',
    'ul_avg_mcs': 'mean',
    'avg_cqi': 'mean',
    'avg_ta_km': 'mean',
    'avg_rssi_dbm': 'mean',
    'outgoing_ho_success_rate_%': 'mean',
    'intra_rat_ho_success_rate_%': 'mean',
    'no_ping_pong_ho_count':'sum'
}).reset_index()

# ==============================================================================
# 🔍 Basic EDA Exploration from aggregated data
# ==============================================================================
basic_EDA_summary(agg_sites_traffic, name ='site level data')
# 🔍 conduct Descriptive analysis for lte_ps_traffic
descriptive_statistics_numeric(agg_sites_traffic, name ='agg_sites_traffic')

# ==============================================================================
# DATA PREPROCESSING of Aggregated Sites Traffic
# ==============================================================================
# 1. Data formatting
# ==============================================================================
agg_sites_traffic.info()
agg_sites_traffic.head()
agg_sites_traffic['timestamp'] = pd.to_datetime(agg_sites_traffic['timestamp'])
agg_sites_traffic.set_index('timestamp', inplace=True)
agg_sites_traffic.info() # Timestamp has become and index

#Exporting the formated and organised data
agg_sites_traffic.to_excel('exports/Libyana LTE KPIs/aggregated_sites_traffic.xlsx')

# 2. Missing Data
# ==============================================================================
# since number of missing data
agg_sites_traffic.shape
agg_sites_traffic=agg_sites_traffic.dropna()
agg_sites_traffic.shape

# 3. CORRELATION ANALYSIS
# ==============================================================================
# ****** Correlation analysis - Per site level
## Computes Pearson correlation (linear relationship) Range: [-1, 1]
TRI022L_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name']=='TRI022L'].select_dtypes(include='number')
corr_TRI022L = TRI022L_numeric.corr(method='pearson')
corr_TRI022L
#Writting Correlation Matrix to disk
corr_TRI022L.to_excel('exports/Libyana LTE KPIs/Correlation/corr_TRI022L.xlsx', index=True)

# 3.1 Creating a correlation Function
def calculate_corr(df, name):
    filtered_df = df[df['enodeb_name'] == name]
    numeric_df = filtered_df.select_dtypes(include='number')
    correlation_matrix = numeric_df.corr()
    return correlation_matrix

# 3.2 Running the correlation function for enodeB
corr_TRI882L = calculate_corr(agg_sites_traffic, name='TRI882L')
corr_TRI022L = calculate_corr(agg_sites_traffic, name='TRI022L')
corr_TRI166L = calculate_corr(agg_sites_traffic, name='TRI166L')
corr_TRI231L = calculate_corr(agg_sites_traffic, name='TRI231L')
corr_TRI878L = calculate_corr(agg_sites_traffic, name='TRI878L')
corr_TRI183L = calculate_corr(agg_sites_traffic, name='TRI183L')
corr_TRI209L = calculate_corr(agg_sites_traffic, name='TRI209L')
corr_TRI165L = calculate_corr(agg_sites_traffic, name='TRI165L')
corr_TRI809L = calculate_corr(agg_sites_traffic, name='TRI809L')
corr_TRI194L = calculate_corr(agg_sites_traffic, name='TRI194L')
corr_TRI435L = calculate_corr(agg_sites_traffic, name='TRI435L')
corr_TRI1007L = calculate_corr(agg_sites_traffic, name='TRI1007L')
corr_TRI695L = calculate_corr(agg_sites_traffic, name='TRI695L')
corr_TRI055L = calculate_corr(agg_sites_traffic, name='TRI055L')
corr_TRI730L = calculate_corr(agg_sites_traffic, name='TRI730L')
corr_TRI825L = calculate_corr(agg_sites_traffic, name='TRI825L')

# 3.3 Correlation Visualisation
# TRI022L
import matplotlib.pyplot as plt
import seaborn as sns
# Plotting correlation heatmap
plt.figure(figsize=(12,7))
sns.heatmap(corr_TRI022L,
            annot=True,                 # Display correlation values inside the heatmap cells
            fmt='.2f',                  # Format the numbers to 2 decimal places
            cmap='coolwarm',            # Diverging color palette from blue to red
            square=True,                # Shrink the color bar to make space for plot
            cbar_kws={'shrink': 0.5},   # Forcing perfect square for visual asthetics
            annot_kws={'fontsize': 6}  # <-- reducing font size inside the boxed for clarity
            )
plt.title('Pair-wise Correlation Matrix for TRI022L') # Set plot title
plt.xticks(rotation= 45, fontsize = 8, ha='right')    # Rotate and align x-axis tick labels
plt.xlabel('KPI Features')
plt.yticks(fontsize = 8)
plt.ylabel('KPI Features')
plt.tight_layout()                                    # Auto-adjust layout to prevent overlap
plt.show()

# using for loop to plot all the sites correlation
# eNodeB Correlation List
enodeb_list = [
    'TRI882L', 'TRI022L', 'TRI166L', 'TRI231L',
    'TRI878L', 'TRI183L', 'TRI209L', 'TRI165L',
    'TRI809L', 'TRI194L', 'TRI435L', 'TRI1007L',
    'TRI695L', 'TRI055L', 'TRI730L', 'TRI825L']

for name in enodeb_list:
    corr_matrix = calculate_corr(agg_sites_traffic, name=name)
    plt.figure(figsize=(12, 7))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        square=True,
        cbar_kws={'shrink': 0.5},
        annot_kws={'fontsize': 6}
    )
    plt.title(f'Pair-wise Correlation Matrix for {name}')
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.xlabel('KPI Features')
    plt.ylabel('KPI Features')
    plt.tight_layout()
    plt.show()

    ###### with export instead of show
    for name in enodeb_list:
        corr_matrix = calculate_corr(agg_sites_traffic, name=name)
        plt.figure(figsize=(12, 7))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            square=True,
            cbar_kws={'shrink': 0.5},
            annot_kws={'fontsize': 6}
        )
        plt.title(f'Pair-wise Correlation Matrix for {name}')
        plt.xticks(rotation=45, fontsize=8, ha='right')
        plt.yticks(fontsize=8)
        plt.xlabel('KPI Features')
        plt.ylabel('KPI Features')
        plt.tight_layout()
        plt.savefig(f'exports/Libyana LTE KPIs/Correlation/Plots/correlation_matrix_{name}.png', dpi=300)
        plt.close()
#-------------------------------------------------------------
# 4. Outlier handling
# site level outlier handling because each sites has unique KPI behaviour
TRI022a = agg_sites_traffic[agg_sites_traffic['enodeb_name']=='TRI022L']
#Hitogram of target Variable for TRI022L
plt.hist(TRI022a['ps_traffic_volume_gb'], color='lightblue', edgecolor='black')
plt.grid(True, alpha = 0.3)
plt.xlabel('No. of RRC Users')
plt.ylabel('Frequency')
plt.show()

TRI022a.loc[TRI022a['ps_traffic_volume_gb'] < 1800, 'ps_traffic_volume_gb'] = 1974.9996

TRI022a['ps_traffic_volume_gb'].plot(figsize=(12,4))
plt.tight_layout()
plt.show()


def plot_faceted_histograms_ps_traffic(df, enodeb_nam):
    subset = df[df['enodeb_name'] == enodeb_name]
    features = ['ps_traffic_volume_gb']
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, feature in zip(axes.flatten(), features):
        ax.hist(subset[feature].dropna(), color='lightblue', edgecolor='black')
        ax.set_title(f'{feature} Distribution', fontsize=10)
        ax.grid(True, alpha=0.3)
    fig.suptitle(f"Histograms for {enodeb_name}", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show(block=True)

# =======  Hitograms
# Function histogram Plots faceted histograms for selected features of a specific eNodeB.
#     Parameters:
#     - data (pd.DataFrame): Dataset with 'enodeb_name' and selected features.
#     - enodeb_name (str): The name of the eNodeB to filter.

def plot_faceted_histograms(df, enodeb_name):
    subset = df[df['enodeb_name'] == enodeb_name]
    features = ['avg_rssi_dbm', 'mean_no_rrc_users', 'dl_avg_mcs', 'dl_prb_available_bandwidth']
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, feature in zip(axes.flatten(), features):
        ax.hist(subset[feature].dropna(), color='lightblue', edgecolor='black')
        ax.set_title(f'{feature} Distribution', fontsize=10)
        ax.grid(True, alpha=0.3)
    fig.suptitle(f"Histograms for {enodeb_name}", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show(block=True)

def plot_faceted_histograms1(df, enodeb_name):
    subset = df[df['enodeb_name'] == enodeb_name]
    features = ['avg_rssi_dbm', 'mean_no_rrc_users', 'dl_avg_mcs', 'dl_prb_available_bandwidth']
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, feature in zip(axes.flatten(), features):
        ax.hist(subset[feature].dropna(), color='lightblue', edgecolor='black')
        ax.set_title(f'{feature} Distribution', fontsize=10)
        ax.grid(True, alpha=0.3)
    fig.suptitle(f"Histograms for {enodeb_name}", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f'exports/Libyana LTE KPIs/Histogram Plots/eNodeB_{enodeb_name}_histo', dpi=300)
    plt.close()

#plotting all graphs
for name in enodeb_list:
    plot_faceted_histograms1(agg_sites_traffic, enodeb_name=name)

# Drops rows containing outliers in numeric columns for a specific eNodeB based on IQR.
#Parameters:
#- df (pd.DataFrame): Full dataset including 'enodeb_name' column.
#- enodeb_name (str): eNodeB to process.
# Returns:pd.DataFrame with outliers removed for the given eNodeB.

def treat_outliers_iqr_per_enodeb(df: pd.DataFrame, enodeb_name: str) -> pd.DataFrame:
    subset = df[df['enodeb_name'] == enodeb_name].copy()
    numeric_cols = subset.select_dtypes(include='number').columns
    for col in numeric_cols:
        Q1 = subset[col].quantile(0.25)
        Q3 = subset[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        subset = subset[(subset[col] >= lower_bound) & (subset[col] <= upper_bound)]
    cleaned_df = df[df['enodeb_name'] != enodeb_name].copy()
    cleaned_df = pd.concat([cleaned_df, subset], ignore_index=True)
    return cleaned_df

TRI022_OR = treat_outliers_iqr_per_enodeb(agg_sites_traffic, 'TRI022L')
TRI022.columns
plt.hist(TRI022_OR['ps_traffic_volume_gb'], color='lightblue', edgecolor='black')
plt.grid(True, alpha = 0.3)
plt.xlabel('No. of RRC Users')
plt.ylabel('Frequency')
plt.show(block=True)
#------------------------------------------------------------------
#Creating a function to subset enodeb
def subset_enodeb (df, name):
    return df[df['enodeb_name']==name]

TRI022_data = subset_enodeb(agg_sites_traffic, 'TRI022L')


# ==============================================================================
# TIME SERIES VISUALIZATION AND ANALYSIS  
# ==============================================================================
import matplotlib.pyplot as plt
## Time-Series EDA visualisation
agg_sites_traffic['enodeb_name'].unique()
#creating a function to subset sites
def subset_enodeb (df,name):
    return df[df['enodeb_name']==name]

agg_sites_traffic.info()
TRI022L.info()
type(TRI022L)
# ==============================================================================
TRI022L = subset_enodeb(agg_sites_traffic, name='TRI022L')
TRI055L = subset_enodeb(agg_sites_traffic, name='TRI055L')
TRI1007L = subset_enodeb(agg_sites_traffic, name='TRI1007L')
TRI165L = subset_enodeb(agg_sites_traffic, name='TRI165L')
TRI166L = subset_enodeb(agg_sites_traffic, name='TRI166L')
TRI183L = subset_enodeb(agg_sites_traffic, name='TRI183L')
TRI194L = subset_enodeb(agg_sites_traffic, name='TRI194L')
TRI209L = subset_enodeb(agg_sites_traffic, name='TRI209L')
TRI231L = subset_enodeb(agg_sites_traffic, name='TRI231L')
TRI435L = subset_enodeb(agg_sites_traffic, name='TRI435L')
TRI695L = subset_enodeb(agg_sites_traffic, name='TRI695L')
TRI730L = subset_enodeb(agg_sites_traffic, name='TRI730L')
TRI809L = subset_enodeb(agg_sites_traffic, name='TRI809L')
TRI825L = subset_enodeb(agg_sites_traffic, name='TRI825L')
TRI878L = subset_enodeb(agg_sites_traffic, name='TRI878L')
TRI882L = subset_enodeb(agg_sites_traffic, name='TRI882L')
# ==============================================================================
TRI022L.to_csv('exports/TRI022L.csv')
#TRI022L TSA EDA - 1 Year
TRI022L['2024-06-01':]['ps_traffic_volume_gb'].plot(figsize=(12, 4))
plt.xlabel("Timestamp")
plt.ylabel("PS Traffic Volume (GB)")
plt.title("PS Traffic Volume for TRI022L")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
# Resampling Mean Monthly to check the trend M: Month, QS: Quarerly, YE: Yearly
TRI022L['ps_traffic_volume_gb'].resample(rule='M').mean().plot(figsize=(12,4))
plt.xlabel("Timestamp")
plt.ylabel("PS Traffic Volume (GB)")
plt.title("PS Traffic Volume for TRI022L Montly Average")
plt.grid(True, which='both' ,alpha=0.3)
plt.tight_layout()
plt.show()

# Simple moving average Smoothing
TRI022L.info()
# Simple moving average Smoothing
TRI022L['ps_30_rolling_window']=TRI022L['ps_traffic_volume_gb'].rolling(15, min_periods =1).mean()
# Cumaltitive average Smoothing
TRI022L['ps_CMA']=TRI022L['ps_traffic_volume_gb'].expanding().mean()
# Expontential average Smoothing
TRI022L['ps_EMA'] = TRI022L['ps_traffic_volume_gb'].ewm(alpha=0.3, adjust=False).mean()
# Expontential weighted average Smoothing
TRI022L['ps_EWMA'] = TRI022L['ps_traffic_volume_gb'].ewm(span=30).mean()

#TRI022L 1 Year TSA EDA + SMA 30 + CMA + EMA + EWMA
TRI022L['2024-06-01':][['ps_traffic_volume_gb',
                        'ps_CMA',
                        'ps_EMA',
                        'ps_EWMA']].plot(figsize=(12, 4))
plt.xlabel("Timestamp")
plt.ylabel("PS Traffic Volume (GB)")
plt.title("PS Traffic Volume for TRI022L & Smoothing Techniques SMA, CMA \n EMA & EWMA ")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ==============================================================================
#  Function to smooth_and_plot_enodeb_traffic to conduce TSA EDA
# ==============================================================================
def plot_ps_traffic_smoothing (df, enodeb_name,
                               SMAwindow=15,
                               ema_alpha=0.3,
                               ewma_span=30,
                               start_date=None,
                               end_date=None):
    site_df = df[df['enodeb_name'] == enodeb_name].copy()
    if start_date and end_date:
        site_df = site_df.loc[start_date:end_date]
    elif start_date:
        site_df = site_df.loc[start_date: ]
    # Calculate moving averages
    site_df['ps_SMA'] = site_df['ps_traffic_volume_gb'].rolling(SMAwindow, min_periods=1).mean()
    site_df['ps_CMA'] = site_df['ps_traffic_volume_gb'].expanding().mean()
    site_df['ps_EMA'] = site_df['ps_traffic_volume_gb'].ewm(alpha=ema_alpha, adjust=False).mean()
    site_df['ps_EWMA'] = site_df['ps_traffic_volume_gb'].ewm(span=ewma_span).mean()
    # Plot
    site_df[['ps_traffic_volume_gb', 'ps_SMA', 'ps_CMA', 'ps_EMA', 'ps_EWMA']].plot(figsize=(12, 4))
    plt.title(f"PS Traffic Volume Smoothing for {enodeb_name}")
    plt.xlabel("Timestamp")
    plt.ylabel("PS Traffic Volume (GB)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# =======================
#Applying the function
for name in enodeb_list:
    plot_ps_traffic_smoothing(agg_sites_traffic, name)

#-----------------
plot_ps_traffic_smoothing(agg_sites_traffic,
                          'TRI022L',
                          7,
                          0.3,
                          30,
                          None,
                          None)

# ==============================================================
# Seasonal-Trend Decomposition using Loess (STL)
# ==============================================================
from statsmodels.tsa.seasonal import STL
# Apply STL decomposition
TRI022L_STL = STL(TRI022L['ps_traffic_volume_gb'], period=7)
TRI022L_STL_result = TRI022L_STL.fit()
# --------------------------------------------------------------
# Plot the STL decomposition for TRI022L
plt.figure(figsize=(14, 10))
TRI022L_STL_result.plot()
plt.xticks(fontsize=8, va='top', rotation =45)
plt.yticks(fontsize =8)
plt.tight_layout()
plt.show()
# --------------------------------------------------------------
# improved Plot the STL decomposition for TRI022L
fig = TRI022L_STL_result.plot()
fig.set_size_inches(14, 10)
# Manually position the x-axis ticks at the bottom for each subplot
fig.axes[0].tick_params(axis='x', bottom=True, labelbottom=True, top=False, labeltop=False)
fig.axes[1].tick_params(axis='x', bottom=True, labelbottom=True, top=False, labeltop=False)
fig.axes[2].tick_params(axis='x', bottom=True, labelbottom=True, top=False, labeltop=False)
# Adjust font size and layout
fig.axes[0].tick_params(axis='x', labelsize=8)
fig.axes[1].tick_params(axis='x', labelsize=8)
fig.axes[2].tick_params(axis='x', labelsize=8)
plt.tight_layout()
plt.show()
# --------------------------------------------------------------
# Creating a function to conduct STL
def plot_stl_decomposition(df, enodeb_name, period=7):
    site_df = df[df['enodeb_name'] == enodeb_name].copy()
    site_df = site_df.sort_index()
    # Apply STL
    stl_result = STL(site_df['ps_traffic_volume_gb'], period=period).fit()
    # Plot
    fig = stl_result.plot()
    fig.set_size_inches(14, 10)
    # Set x-axis ticks below and adjust formatting
    for ax in fig.axes:
        ax.tick_params(axis='x', bottom=True, labelbottom=True, top=False, labeltop=False)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Allow room for suptitle
    fig.suptitle(f'STL Decomposition of PS Traffic Volume – {enodeb_name} - {period} Days', fontsize=14)
    plt.show()
# --------------------------------------------------------------
plot_stl_decomposition(agg_sites_traffic, 'TRI022L') # default period is 7 defined in the function
plot_stl_decomposition(agg_sites_traffic, 'TRI022L', 30)
# Apply here for more eNodeBs >>>>
# >>> Group 2
plot_stl_decomposition(agg_sites_traffic, 'TRI166L', 7)
plot_stl_decomposition(agg_sites_traffic, 'TRI231L', 7)
plot_stl_decomposition(agg_sites_traffic, 'TRI878L', 7)
plot_stl_decomposition(agg_sites_traffic, 'TRI183L', 7)

# --------------------------------------------------------------
# ==============================================================
# Expontiontial Smoothing & Holt-winters
# ==============================================================

from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
#Simple Expontiontial Smoothing
ses_TRI022LS = SimpleExpSmoothing(TRI022L_train['ps_traffic_volume_gb']).fit()
ses_TRI022LS.summary()

ses_TRI022LS.info()
ses_TRI022LS

# ==============================================================
# Data Preparation Hypothesis Testing - Stationarity Check
# ==============================================================
from statsmodels.tsa.stattools import adfuller # Augmented Dicky-Fuller (ADF) test

#✅ Null Hypothesis (H₀): The series has a unit root (non-stationary)
#❌ Alternative Hypothesis (H₁): The series is stationary and has no unit root
# --------------------------------------------------------------
# Creating ADfuller function to test for stationary
# --------------------------------------------------------------
def adfuller_test(series):
    result = adfuller(series)
    print('Augmented Dicky-Fuller (ADF) test statistic:{}'.format(result[0]))
    print('p-Value: {}'.format(result[1]))
    if result[1] < 0.05:
        print('Strong evidence against the null hypothesis. Reject the null hypothesis & data is stationary')
    else:
        print('Weak Evidence againest the null hypothesis. Reject the alternative hypothesis and data is not stationary')
# --------------------------------------------------------------
# Run the ADF test on TRI022L ps traffic
adfuller_test(TRI022L['ps_traffic_volume_gb']) #Not Sationary >>>> require Differencing

# >> 1st Differencing for TRI022 ps_traffic
TRI022L.loc[:,'ps_traffic_Diff1'] = TRI022L['ps_traffic_volume_gb']-TRI022L['ps_traffic_volume_gb'].shift(1)

# >> Running the test again
adfuller_test(TRI022L['ps_traffic_Diff1'].dropna()) # Data is stationary now

# >> Manually plotting the the first Difference for TRI022L along with the trend
TRI022L[['ps_traffic_volume_gb','ps_traffic_Diff1']].plot(figsize=(12,4))
plt.xticks(rotation=45)
plt.grid(True, alpha=0.2, color='grey')
plt.tight_layout()
plt.show()
# ------------------------------------------------------
# Creating a plotting function Trend+Diff & Differencing Function
# ------------------------------------------------------
#Plot Trend + Differenced
def plot_trend_Diff(df, diff_level=1, col='ps_traffic_volume_gb', prefix='ps_traffic_Diff'):
    diff_col = f"{prefix}{diff_level}"
    if diff_col not in df.columns:
        print(f"Column '{diff_col}' not found. Please generate it before plotting.")
        return
    enodeb_name = df['enodeb_name'].unique()[0] if 'enodeb_name' in df.columns else "Unknown eNodeB"
    df[[col, diff_col]].plot(figsize=(14, 5))
    plt.title(f'PS Traffic Volume and {diff_col} for {enodeb_name}')
    plt.xlabel('Timestamp')
    plt.ylabel('Traffic Volume / Difference')
    plt.grid(True, alpha=0.2, color='grey')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# >>>>>
#Applying the plot_trend_Diff to TRI022L
plot_trend_Diff(TRI022L, 12)
# ---------------------------------------------------------------
# Creating Differencing Function and appending the result to existing datafram
# ------------------------------------------------------
def add_diff_column(df, col='ps_traffic_volume_gb', prefix='ps_traffic_Diff'):
    existing = [int(c.replace(prefix, '')) for c in df.columns if c.startswith(prefix) and c.replace(prefix, '').isdigit()]
    next_diff = max(existing) + 1 if existing else 1
    base_col = f"{prefix}{next_diff - 1}" if next_diff > 1 else col
    df[f"{prefix}{next_diff}"] = df[base_col].diff()
    return df

# ---------------------------------------------------------------
# Function that Iterates the running of Differecing function of a given number
def run_add_diff_column_for_n_times(add_diff_column, df, n, **kwargs):
    for _ in range(n):
        df = add_diff_column(df, **kwargs)
    return df

# >>>>> running the function creating 12 differences for group 2 sites

run_add_diff_column_for_n_times(add_diff_column, TRI022L, 12) # Diff1 & Diff2
TRI022L.info()
plot_trend_Diff(TRI022L, 1)

run_add_diff_column_for_n_times(add_diff_column, TRI166L, 12)
plot_trend_Diff(TRI166L, 1)

run_add_diff_column_for_n_times(add_diff_column, TRI231L, 12)
plot_trend_Diff(TRI022L, 1)

run_add_diff_column_for_n_times(add_diff_column, TRI878L, 12)
plot_trend_Diff(TRI231L, 1)

run_add_diff_column_for_n_times(add_diff_column, TRI183L, 12)
plot_trend_Diff(TRI183L, 1)

# ---------------------------------------------------------------

# Checking the ADF test all sites became sationary after the first differencing
adfuller_test(TRI166L['ps_traffic_Diff1'].dropna())
adfuller_test(TRI231L['ps_traffic_Diff1'].dropna())
adfuller_test(TRI878L['ps_traffic_Diff1'].dropna())
adfuller_test(TRI183L['ps_traffic_Diff1'].dropna())

# ==============================================================
# Autocorrelation ACF and Partial Auto Correlation
# ==============================================================
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# >>>>> ACF Plot
plt.subplots(figsize=(5, 5))
plot_acf(TRI022L['ps_traffic_Diff1'].dropna())
plt.title('ACF Plot for TRI022')
plt.grid(True, alpha = 0.09, color ='grey')
plt.tight_layout()
plt.show()

# >>>>> PACF Plot
plt.subplots(figsize=(5, 5))
plot_pacf(TRI022L['ps_traffic_Diff1'].dropna())
plt.title('PACF Plot for TRI022 Diff1')
plt.grid(True, alpha = 0.09, color ='grey')
plt.tight_layout()
plt.show()
# -----------------------------------------------------
# Creating A function for Plotting ACF and PACF
# ACF Plotting Function
def func_plot_acf(df, col_name, site_label=""):
    plt.subplots(figsize=(5, 5))
    plot_acf(df[col_name].dropna())
    plt.title(f'ACF Plot for {site_label} for {col_name}')
    plt.grid(True, alpha=0.09, color='grey')
    plt.tight_layout()
    plt.show()
# PACF Plotting Function
def func_plot_pacf(df, col_name, site_label=""):
    plt.subplots(figsize=(5, 5))
    plot_acf(df[col_name].dropna())
    plt.title(f'PACF Plot for {site_label} for {col_name}')
    plt.grid(True, alpha=0.09, color='grey')
    plt.tight_layout()
    plt.show()
# ---------------------------
# >>>>> applyting the ACF and PACF plotting for
# > TRI022L
func_plot_acf(TRI022L, 'ps_traffic_Diff1', 'TRI022')
func_plot_pacf(TRI022L, 'ps_traffic_Diff1', 'TRI022')
# ------------------------------------------------------------
# ==============================================================
# Data Splitting : Training and Test
# ==============================================================
TRI022L.index.min() # to get the start Date
TRI022L.index.max() # to get the end date
# > Set the
# training end date and test start date
from datetime import datetime, timedelta
train_end = datetime(2025,2,28) # 9 months train    /#2025-04-30 --11M
test_end = datetime(2025, 6,24) # 3.8 months test /#2025-05-01 --2M
# > Apply the splitting
TRI022L_train = TRI022L[: train_end]
TRI022L_test = TRI022L[train_end+timedelta(days=1): test_end]

TRI022L_train.index.max()
TRI022L_test.index.min()

# ---- > Building ARIMA Model
# building the model
from statsmodels.tsa.arima.model import ARIMA
#>
TRI022L_ARIMA = ARIMA(TRI022L_train['ps_traffic_volume_gb'],
                      order=(7,1,20))
#>
TRI022L_ARIMA_fit = TRI022L_ARIMA.fit()
#>
TRI022L_ARIMA_fit.summary()
# >>> Making Prediction
predict_start_date =TRI022L_test.index[0]
predict_end_date =TRI022L_test.index[-1]
predict_future = predict_end_date+timedelta(days=200)

predict_start_date
predict_end_date
predict_future

TRI022L_pred =TRI022L_ARIMA_fit.predict(start=predict_start_date,
                                       end=predict_end_date,
                                        typ='levels')

TRI022L_pred.head(10)
# Plot

plt.figure(figsize=(14, 5))
plt.plot(TRI022L_train['ps_traffic_volume_gb'], label='Training')
plt.plot(TRI022L_test['ps_traffic_volume_gb'], label='Actual (Test)')
plt.plot(forecast_df['mean'], label='Forecast', linestyle='--', color='green')
plt.fill_between(forecast_df.index,
                 forecast_df['mean_ci_lower'],
                 forecast_df['mean_ci_upper'],
                 color='green', alpha=0.2)
plt.title('Daily Forecast vs Actual for TRI022L – ARIMA(7,1,20)')
plt.xlabel('Date')
plt.ylabel('PS Traffic Volume (GB)')
plt.legend()
plt.tight_layout()
plt.show()

#------------- SARIMAX
from statsmodels.tsa.statespace.sarimax import SARIMAX

sarima_model = SARIMAX(TRI022L_train['ps_traffic_volume_gb'],
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 7),
                enforce_stationarity=False,
                enforce_invertibility=False)

sarima_model_fit = sarima_model.fit()
sarima_model_fit.summary()

TRI022L_pred_sarima =sarima_model_fit.predict(start=predict_start_date,
                                       end=predict_end_date,
                                        typ='levels')
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))
plt.plot(TRI022L_train['ps_traffic_volume_gb'], label='Training')
plt.plot(TRI022L_test['ps_traffic_volume_gb'], label='Actual (Test)', color='orange')
plt.plot(TRI022L_pred_sarima, label='Forecast', color='green', linestyle='--')
plt.title('SARIMAX Forecast vs Actual – TRI022L')
plt.xlabel('Date')
plt.ylabel('PS Traffic Volume (GB)')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
sarima_model_fit.resid.plot(kind='kde')
plt.tight_layout()
plt.show()

# >>> predict future
TRI022L_pred_sarima_future =sarima_model_fit.predict(start=predict_start_date,
                                       end=predict_future,
                                        typ='levels')
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))
plt.plot(TRI022L_train['ps_traffic_volume_gb'], label='Training')
plt.plot(TRI022L_test['ps_traffic_volume_gb'], label='Actual (Test)', color='orange')
plt.plot(TRI022L_pred_sarima_future, label='Forecast', color='green', linestyle='--')
plt.title('SARIMAX Forecast vs Actual – TRI022L')
plt.xlabel('Date')
plt.ylabel('PS Traffic Volume (GB)')
plt.legend()
plt.tight_layout()
plt.show()

# Again
TRI022L_train
TRI022L_test

# This time using pmdarim
from pmdarima import

#  MAE, RMSE and MSE MAPE
from sklearn.metrics import root_mean_squared_error, mean_squared_error, mean_absolute_error,mean_absolute_percentage_error

print(root_mean_squared_erro(f" RMSE:{rmse:.f}")
print(mean_absolute_error(f" MAE:{mae:.f}")
print(mean_absolute_percentage_error(f" MAPE:{mape:.f}")
