# **** importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display_functions import display
from IPython.core.display_functions import display
from jedi.api.refactoring import inline
#------------------------------------------------------------------------------
## **** Setting the pd configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
#-------------------------------------------------------------------------------
## 📁 importing Libyana LTE KPI Data
lte_rawdata = pd.read_excel('Datasets/Libyana Dataset JUN25/History Query-LTE KPI one year daily.xlsx',
                            sheet_name='Sheet0')
#--------------------------------------------------------------------------------------------------------
# ⚙️️ EDA summary function with Export feature
def basic_EDA_Summary(df, name="DataFrame"):
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
# -------------------------------------------------------------------------------------------------------------------
# 🔍 Exploring lte raw data EDA Summary
basic_EDA_Summary(lte_rawdata, name="LTE Raw Data")
# 🔍 checking how many LTE enodeB
lte_rawdata['eNodeB Name'].unique()
lte_rawdata['eNodeB Name'].nunique()
lte_rawdata['eNodeB Name'].value_counts()
# 🔍 checking how many LTE Cells
lte_rawdata['E-UTRAN FDD Cell Name'].unique()
lte_rawdata['E-UTRAN FDD Cell Name'].nunique()
lte_rawdata['E-UTRAN FDD Cell Name'].value_counts().to_csv('exports/noofcellsobsercations.csv')
#-----------------------------------------------------------------------------------
##### ***** Select KEY Radio Features required for forecasting PS traffic
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
#------------------------------------------------------------------------------------------
# 🔍 Exploring lte_ps_traffic EDA Summary
basic_EDA_Summary2(lte_ps_traffic, name = 'lte ps traffic')
# 🔍 checking how many LTE enodeB
lte_rawdata['enodeb_name'].unique()
lte_rawdata['enodeb_name'].nunique()
lte_rawdata['enodeb_name'].value_counts()
# 🔍 checking how many LTE Cells
lte_rawdata['cell_name'].unique()
lte_rawdata['cell_name'].nunique()
lte_rawdata['cell_name'].value_counts().to_csv('exports/ltepstraffi_countofcells.csv')
#-------------------------------------------------------------------------------------------------------------------
# ⚙️️ Summary statistics Function
    #Computes descriptive statistics for all numeric columns and exports to Excel.
    # Parameters:
    # - df: DataFrame containing data
    # - name: String name to label output (used in messages and default path)
    # - file_path: Optional path to save Excel output (default uses name)
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
#--------------------------------------------------------------------------------------------------------------------
# 🔍 Exploring lte raw data EDA Summary
descriptive_statistics_numeric(lte_ps_traffic, name ='lte_ps_traffic')
#---------------------------------------------------------------------------------------------------------------
lte_ps_traffic[lte_ps_traffic['enodeb_name']=='TRI882L']
lte_ps_traffic[lte_ps_traffic['cell_name']=='TRI882L-1']

lte_ps_traffic[lte_ps_traffic['enodeb_name']=='TRI435L']
lte_ps_traffic[lte_ps_traffic['cell_name']=='TRI435L-1']

# Rename index to 'Column' and convert it into a column in the DataFrame
lte_ps_traffic_summary_statistics.index.name = 'Feature'
lte_ps_traffic_summary_statistics.reset_index(inplace=True)
#Exporting the Statitics to local Disk
lte_ps_traffic_summary_statistics
lte_ps_traffic_summary_statistics.to_excel("exports/Libyana LTE KPIs/lte_ps_traffic_summary_statistics.xlsx", index=False)

## **** for time series modify the data type for timestamp feature
lte_ps_traffic['timestamp'] = pd.to_datetime(lte_ps_traffic['timestamp'])
lte_ps_traffic['timestamp'].dtype

lte_ps_traffic.to_excel('exports/lte_ps_traffic.xlsx')

# ***** Group by timestamp and enodeb_name, and aggregate using appropriate functions
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
    'no_ping_pong_ho_count': 'sum'
}).reset_index()

agg_sites_traffic.to_excel('exports/Libyana LTE KPIs/aggregated_sites_traffic.xlsx')

agg_sites_traffic['timestamp'] = pd.to_datetime(agg_sites_traffic['timestamp'])
agg_sites_traffic.set_index('timestamp', inplace=True)
agg_sites_traffic

# ****** Descriptive Statistics - Per site level
TRI022L_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == 'TRI022L'].select_dtypes(include='number')

TRI022L_Summary_stats = pd.DataFrame({
    'Min': TRI022L_numeric.min(),
    'Max': TRI022L_numeric.max(),
    'Mean': TRI022L_numeric.mean(),
    'Std. Deviation': TRI022L_numeric.std(),
    'Variance': TRI022L_numeric.var(),
    'Skewness': TRI022L_numeric.skew(),
    'Kurtosis': TRI022L_numeric.kurtosis(),
    'Sum': TRI022L_numeric.sum(),
    'Median': TRI022L_numeric.median(),
    'Missing': TRI022L_numeric.isna().sum(),
    'Row count': len(TRI022L_numeric)
})

TRI022L_Summary_stats.index.name='Feature'
TRI022L_Summary_stats

### iterate the computation of summary statistics for all numeric KPIs
# Initialize a list to store summary statistics DataFrames for each eNodeB
summary_stats_list = []
# Loop through each unique eNodeB in the dataset
for enodeb in agg_sites_traffic['enodeb_name'].unique():
    enodeb_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == enodeb].select_dtypes(include='number')
    # Compute summary statistics for each numeric column
    stats = pd.DataFrame({
        'Min': enodeb_numeric.min(),
        'Max': enodeb_numeric.max(),
        'Mean': enodeb_numeric.mean(),
        'Std. Deviation': enodeb_numeric.std(),
        'Variance': enodeb_numeric.var(),
        'Skewness': enodeb_numeric.skew(),
        'Kurtosis': enodeb_numeric.kurtosis(),
        'Sum': enodeb_numeric.sum(),
        'Median': enodeb_numeric.median(),
        'Missing': enodeb_numeric.isna().sum(),
        'Row count': len(enodeb_numeric)
    })

    stats.index.name = 'Feature'
    stats['eNodeB'] = enodeb
    summary_stats_list.append(stats.reset_index())

# Combine all into one DataFrame
all_summary_stats = pd.concat(summary_stats_list)
all_summary_stats = all_summary_stats.set_index(['eNodeB', 'Feature'])

all_summary_stats.to_csv('exports/Libyana LTE KPIs/stats_enodeB.csv')

# ****** Correlation analysis - Per site level
## === Correlation Analysis
#Computes Pearson correlation (linear relationship) Range: [-1, 1]
corr_TRI022L = TRI022L_numeric.corr(method='pearson')
#Writting Correlation Matrix to disk
corr_TRI022L.to_excel('exports/Libyana LTE KPIs/Correlation/corr_TRI022L.xlsx', index=True)

# Create a Pandas ExcelWriter to hold multiple sheets
with pd.ExcelWriter('exports/Libyana LTE KPIs/Correlation/enodeb_correlations.xlsx', engine='xlsxwriter') as writer:
    # Loop through each unique eNodeB
    for enodeb in agg_sites_traffic['enodeb_name'].unique():
        # Select numeric data for current eNodeB
        enodeb_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == enodeb].select_dtypes(include='number')

        # Skip if there are fewer than 2 numeric columns (correlation not possible)
        if enodeb_numeric.shape[1] < 2:
            continue

        # Compute Pearson correlation matrix
        corr_matrix = enodeb_numeric.corr(method='pearson')

        # Write correlation matrix to a sheet named after the eNodeB
        # Sheet names must be 31 characters or fewer and cannot contain certain characters
        safe_sheet_name = enodeb[:31].replace('/', '_')
        corr_matrix.to_excel(writer, sheet_name=safe_sheet_name)

## Correlation Visualisation
import matplotlib.pyplot as plt
import seaborn as sns
# Plotting correlation heatmap
plt.figure(figsize=(35,25))
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
plt.show(block= True)










### plotting Time-Series relationship for all sites
agg_sites_traffic['enodeb_name'].unique()
#TRI022L
agg_sites_traffic[agg_sites_traffic['enodeb_name']=='TRI022L']['ps_traffic_volume_gb'].plot(grid=True,
                                                                                            figsize=(12, 5),
                                                                                            title='Total PS Traffic Volume Over Time')
plt.xlabel('Timestamp')
plt.ylabel('PS Traffic Volume (GB)')
plt.tight_layout()
plt.show(block=True)

#TRI022 1 month KPIs
#TRI022L
agg_sites_traffic[agg_sites_traffic['enodeb_name']=='TRI022L']['ps_traffic_volume_gb'].plot(grid=True,
                                                                                            xlim=['2024-06-01','2024-08-30'],
                                                                                            figsize=(12, 5),
                                                                                            title='Total PS Traffic Volume Over Time')
plt.xlabel('Timestamp')
plt.ylabel('PS Traffic Volume (GB)')
plt.tight_layout()
plt.show(block=True)

# plot iteratin using a for loop to plot for all enodebs
for site in agg_sites_traffic['enodeb_name'].unique():
    agg_sites_traffic[agg_sites_traffic['enodeb_name'] == site]['ps_traffic_volume_gb'].plot(
        grid=True,
        figsize=(12, 5),
        title=f'Total PS Traffic Volume Over Time – {site}'
    )
    plt.xlabel('Timestamp')
    plt.ylabel('PS Traffic Volume (GB)')
    plt.tight_layout()
    plt.show(block=True)
# to filter a specific year
agg_sites_traffic.loc['2024']


lte_ps_traffic.info()


# ****** ARIMA Model : predicted individual Sites traffic based on aggrageted cells traffic

#### correlation iternation and export
# Create a Pandas ExcelWriter to hold multiple sheets
with pd.ExcelWriter('exports/Libyana LTE KPIs/Correlation/enodeb_correlations.xlsx', engine='xlsxwriter') as writer:
    # Loop through each unique eNodeB
    for enodeb in agg_sites_traffic['enodeb_name'].unique():
        # Select numeric data for current eNodeB
        enodeb_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == enodeb].select_dtypes(include='number')

        # Skip if there are fewer than 2 numeric columns (correlation not possible)
        if enodeb_numeric.shape[1] < 2:
            continue

        # Compute Pearson correlation matrix
        corr_matrix = enodeb_numeric.corr(method='pearson')

        # Write correlation matrix to a sheet named after the eNodeB
        # Sheet names must be 31 characters or fewer and cannot contain certain characters
        safe_sheet_name = enodeb[:31].replace('/', '_')
        corr_matrix.to_excel(writer, sheet_name=safe_sheet_name)

# ****** Descriptive Statistics - Per site level
descriptive_statistics_numeric(agg_sites_traffic[agg_sites_traffic['enodeb_name'] == 'TRI022L'], name='TRI022')

TRI022L_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == 'TRI022L'].select_dtypes(include='number')

TRI022L_Summary_stats = pd.DataFrame({
    'Min': TRI022L_numeric.min(),
    'Max': TRI022L_numeric.max(),
    'Mean': TRI022L_numeric.mean(),
    'Std. Deviation': TRI022L_numeric.std(),
    'Variance': TRI022L_numeric.var(),
    'Skewness': TRI022L_numeric.skew(),
    'Kurtosis': TRI022L_numeric.kurtosis(),
    'Sum': TRI022L_numeric.sum(),
    'Median': TRI022L_numeric.median(),
    'Missing': TRI022L_numeric.isna().sum(),
    'Row count': len(TRI022L_numeric)
})

TRI022L_Summary_stats.index.name = 'Feature'
TRI022L_Summary_stats


def descriptive_stat_sitelevel(df, name: str) -> pd.DataFrame:
    filtered_df = df[df['enodeb_name'] == name],
    numeric_df = filtered_df.select_dtypes(include='number')
    'Min': TRI022L_numeric.min(),
    'Max': TRI022L_numeric.max(),
    'Mean': TRI022L_numeric.mean(),
    'Std. Deviation': TRI022L_numeric.std(),
    'Variance': TRI022L_numeric.var(),
    'Skewness': TRI022L_numeric.skew(),
    'Kurtosis': TRI022L_numeric.kurtosis(),
    'Sum': TRI022L_numeric.sum(),
    'Median': TRI022L_numeric.median(),
    'Missing': TRI022L_numeric.isna().sum(),
    'Row count': len(TRI022L_numeric)}

    ### iterate the computation of summary statistics for all numeric KPIs
    # Initialize a list to store summary statistics DataFrames for each eNodeB
    summary_stats_list = []
    # Loop through each unique eNodeB in the dataset
    for enodeb in agg_sites_traffic['enodeb_name'].unique():
        enodeb_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == enodeb].select_dtypes(include='number')
    # Compute summary statistics for each numeric column
    stats = pd.DataFrame({
        'Min': enodeb_numeric.min(),
        'Max': enodeb_numeric.max(),
        'Mean': enodeb_numeric.mean(),
        'Std. Deviation': enodeb_numeric.std(),
        'Variance': enodeb_numeric.var(),
        'Skewness': enodeb_numeric.skew(),
        'Kurtosis': enodeb_numeric.kurtosis(),
        'Sum': enodeb_numeric.sum(),
        'Median': enodeb_numeric.median(),
        'Missing': enodeb_numeric.isna().sum(),
        'Row count': len(enodeb_numeric)
    })

    stats.index.name = 'Feature'
    stats['eNodeB'] = enodeb
    summary_stats_list.append(stats.reset_index())

    # Combine all into one DataFrame

    enode_bsummary_stats = pd.concat(summary_stats_list)

    all_summary_stats = all_summary_stats.set_index(['eNodeB', 'Feature'])

    all_summary_stats.to_csv('exports/Libyana LTE KPIs/stats_enodeB.csv')

    # ****** Correlation analysis - Per site level
    ## === Correlation Analysis
    # #Computes Pearson correlation (linear relationship) Range: [-1, 1]
    TRI022L_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == 'TRI022L'].select_dtypes(include='number')
    corr_TRI022L = TRI022L_numeric.corr(method='pearson')
    corr_TRI022L
    # Writting Correlation Matrix to disk
    corr_TRI022L.to_excel('exports/Libyana LTE KPIs/Correlation/corr_TRI022L.xlsx', index=True)
    # ------


def calculate_corr(df, name: str) -> pd.DataFrame:
    filtered_df = df[df['enodeb_name'] == name]
    numeric_df = filtered_df.select_dtypes(include='number')
    correlation_matrix = numeric_df.corr()
    return correlation_matrix


#
corr_TRI022L = calculate_corr(agg_sites_traffic, name='TRI022L')

# Create a Pandas ExcelWriter to hold multiple sheets
with pd.ExcelWriter('exports/Libyana LTE KPIs/Correlation/enodeb_correlations.xlsx', engine='xlsxwriter') as writer:
    # Loop through each unique eNodeB
    for enodeb in agg_sites_traffic['enodeb_name'].unique():
        # Select numeric data for current eNodeB
        enodeb_numeric = agg_sites_traffic[agg_sites_traffic['enodeb_name'] == enodeb].select_dtypes(include='number')

        # Skip if there are fewer than 2 numeric columns (correlation not possible)
        if enodeb_numeric.shape[1] < 2:
            continue

        # Compute Pearson correlation matrix
        corr_matrix = enodeb_numeric.corr(method='pearson')

        # Write correlation matrix to a sheet named after the eNodeB
        # Sheet names must be 31 characters or fewer and cannot contain certain characters
        safe_sheet_name = enodeb[:31].replace('/', '_')
        corr_matrix.to_excel(writer, sheet_name=safe_sheet_name)



## Correlation Visualisation
import matplotlib.pyplot as plt
import seaborn as sns
# Plotting correlation heatmap
plt.figure(figsize=(35,25))
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
plt.show(block= True)



# plot iteratin using a for loop to plot for all enodebs
for site in agg_sites_traffic['enodeb_name'].unique():
    agg_sites_traffic[agg_sites_traffic['enodeb_name'] == site]['ps_traffic_volume_gb'].plot(
        grid=True,
        figsize=(12, 5),
        title=f'Total PS Traffic Volume Over Time – {site}'
    )
    plt.xlabel('Timestamp')
    plt.ylabel('PS Traffic Volume (GB)')
    plt.tight_layout()
    plt.show(block=True)
# to filter a specific year
agg_sites_traffic.loc['2024-06-10']

lte_ps_traffic.info()


#### outlier histogram

def plot_faceted_histograms(data: pd.DataFrame, enodeb_name: str):
    subset = data[data['enodeb_name'] == enodeb_name]
    features = ['avg_rssi_dbm', 'mean_no_rrc_users', 'dl_avg_mcs', 'dl_prb_available_bandwidth']
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, feature in zip(axes.flatten(), features):
        ax.hist(subset[feature].dropna(), color='lightblue', edgecolor='black')
        ax.set_title(f'{feature} Distribution', fontsize=10)
        ax.grid(True, alpha=0.3)
    fig.suptitle(f"Histograms for {enodeb_name}", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show(block=True)


plot_faceted_histograms(agg_sites_traffic, enodeb_name='TRI022L')
plot_faceted_histograms(agg_sites_traffic, enodeb_name='TRI1007L')