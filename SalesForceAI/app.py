import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SalesForce AI | Topic 7", page_icon="📊", layout="wide")
st.title("📊 SalesForce AI")
st.caption("Topic 7: AI in Sales Performance Management | MBA / PGDM Student Project")
st.info("This is a usable student prototype. It calculates performance metrics and gives rule-based coaching suggestions. It is not a trained AI model.")

COLS = ["Executive","Territory","Target","Actual_Sales","Total_Calls","Productive_Calls","Planned_Outlets","Outlets_Visited","Orders","Previous_Sales","Variable_Cost","Territory_Expenses"]

def sample():
    return pd.DataFrame([
        ["Arjun","North Madurai",1000000,1200000,50,30,20,18,25,1100000,420000,70000],
        ["Ravi","East Madurai",1000000,950000,60,24,25,20,22,900000,304000,35000],
        ["Karthik","West Madurai",900000,1080000,55,33,22,21,27,950000,390000,50000],
        ["Bala","Central Madurai",1100000,880000,70,28,30,24,20,920000,330000,60000],
        ["Deepak","South Madurai",850000,1020000,48,29,20,19,24,800000,360000,40000],
    ], columns=COLS)

def analyse(raw):
    d = raw.copy()
    nums = [c for c in COLS if c not in ["Executive","Territory"]]
    for c in nums: d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0)
    d["Quota_Achievement_%"] = np.where(d.Target>0, d.Actual_Sales/d.Target*100, 0)
    d["Strike_Rate_%"] = np.where(d.Total_Calls>0, d.Productive_Calls/d.Total_Calls*100, 0)
    d["Outlet_Coverage_%"] = np.where(d.Planned_Outlets>0, d.Outlets_Visited/d.Planned_Outlets*100, 0)
    d["Sales_Per_Call"] = np.where(d.Total_Calls>0, d.Actual_Sales/d.Total_Calls, 0)
    d["Average_Order_Value"] = np.where(d.Orders>0, d.Actual_Sales/d.Orders, 0)
    d["Sales_Growth_%"] = np.where(d.Previous_Sales>0, (d.Actual_Sales-d.Previous_Sales)/d.Previous_Sales*100, 0)
    d["Contribution"] = d.Actual_Sales-d.Variable_Cost
    d["Territory_Profit"] = d.Contribution-d.Territory_Expenses
    q=d["Quota_Achievement_%"].clip(0,120)
    sr=(d["Strike_Rate_%"]/50*100).clip(0,120)
    oc=(d["Outlet_Coverage_%"]/90*100).clip(0,120)
    spc=(d["Sales_Per_Call"]/10000*100).clip(0,120)
    con=(d["Contribution"]/150000*100).clip(0,120)
    d["Performance_Score"]=q*.40+sr*.20+oc*.15+spc*.15+con*.10
    def bonus(x):
        return 0 if x<70 else 2000 if x<85 else 4000 if x<100 else 6000 if x<110 else 8000
    d["Illustrative_Incentive"]=d.Performance_Score.apply(bonus)
    def advice(r):
        if r["Quota_Achievement_%"] < 80: return "Review target, territory potential, product availability and account-level opportunities."
        if r["Strike_Rate_%"] <40: return "Coach prospect selection, call planning and conversion of conversations into orders."
        if r["Outlet_Coverage_%"] <80: return "Improve route planning and visit high-potential outlets consistently."
        if r["Territory_Profit"]<0: return "Review costs, discounting and territory expenses."
        if r ["Performance_Score"] >=100: return "Recognise performance; coach to sustain profitable growth and repeat business."
        return "Agree on one improvement area and review progress weekly."
    d["Coaching_Recommendation"]=d.apply(advice,axis=1)
    return d

with st.sidebar:
    st.header("Data")
    file=st.file_uploader("Upload CSV or Excel",type=["csv","xlsx"])
    st.download_button("Download sample CSV",sample().to_csv(index=False).encode(), "sample_sales_data.csv","text/csv")
    st.divider()
    st.caption("Illustrative incentive slabs")
    st.write("Score below 70: ₹0")
    st.write("70–84.9: ₹2,000")
    st.write("85–99.9: ₹4,000")
    st.write("100–109.9: ₹6,000")
    st.write("110+: ₹8,000")

if file:
    try: raw=pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
    except Exception as e:
        st.error(f"Unable to read file: {e}"); st.stop()
else:
    raw=sample()
    st.warning("Sample data is displayed. Upload your own data for actual analysis.")

missing=[c for c in COLS if c not in raw.columns]
if missing:
    st.error("Missing columns: "+", ".join(missing))
    st.write("Required columns:",COLS); st.stop()
d=analyse(raw[COLS])
if d.empty: st.warning("No records found."); st.stop()

zones=["All"]+sorted(d.Territory.astype(str).unique())
zone=st.selectbox("Territory filter",zones)
v=d if zone=="All" else d[d.Territory.astype(str)==zone]

st.subheader("Management overview")
a,b,c,e=st.columns(4)
a.metric("Sales executives",len(v))
b.metric("Total sales",f"₹{v.Actual_Sales.sum():,.0f}")
c.metric("Average quota achievement",f"{v['Quota_Achievement_%'].mean():.1f}%")
e.metric("Territory profit",f"₹{v.Territory_Profit.sum():,.0f}")

st.subheader("Sales performance scorecard")
display=["Executive","Territory","Actual_Sales","Quota_Achievement_%","Strike_Rate_%","Outlet_Coverage_%","Contribution","Territory_Profit","Performance_Score","Illustrative_Incentive"]
st.dataframe(v[display].style.format({
"Actual_Sales":"₹{:,.0f}","Quota_Achievement_%":"{:.1f}%","Strike_Rate_%":"{:.1f}%","Outlet_Coverage_%":"{:.1f}%","Contribution":"₹{:,.0f}","Territory_Profit":"₹{:,.0f}","Performance_Score":"{:.1f}","Illustrative_Incentive":"₹{:,.0f}"
}),use_container_width=True)

l,r=st.columns(2)
with l:
    st.subheader("Actual sales vs target")
    st.bar_chart(v.set_index("Executive")[["Target","Actual_Sales"]])
with r:
    st.subheader("Performance score")
    st.bar_chart(v.set_index("Executive")[["Performance_Score"]])

st.subheader("Individual coaching report")
name=st.selectbox("Select sales executive",v.Executive.astype(str).tolist())
p=v[v.Executive.astype(str)==name].iloc[0]
x,y,z=st.columns(3)
x.metric("Quota achievement",f"{p['Quota_Achievement_%']:.1f}%")
y.metric("Strike rate",f"{p['Strike_Rate_%']:.1f}%")
z.metric("Illustrative incentive",f"₹{p['Illustrative_Incentive']:,.0f}")
st.success(p.Coaching_Recommendation)

with st.expander("Metric formulas and scoring logic"):
    st.markdown("""
    - Quota achievement = Actual sales ÷ Target × 100
    - Strike rate = Productive calls ÷ Total calls × 100
    - Outlet coverage = Outlets visited ÷ Planned outlets × 100
    - Sales per call = Actual sales ÷ Total calls
    - Average order value = Actual sales ÷ Orders
    - Sales growth = (Current sales − Previous sales) ÷ Previous sales × 100
    - Contribution = Sales revenue − Variable costs
    - Territory profit = Contribution − Territory expenses
    - Performance score = Quota 40% + Strike rate 20% + Outlet coverage 15% + Sales per call 15% + Contribution 10%. Each component is capped at 120 for scoring.
    """)
st.download_button("Download analysed results",d.to_csv(index=False).encode(),"salesforce_ai_analysis.csv","text/csv")
st.caption("Academic demonstration only. Sample data and incentive slabs are assumptions, not company policy. Current recommendations use business rules, not a trained machine-learning model.")
