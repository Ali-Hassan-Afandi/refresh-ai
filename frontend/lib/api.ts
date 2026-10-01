const API=process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000";
async function req(path:string,init?:RequestInit){const r=await fetch(`${API}${path}`,{...init,cache:"no-store"});if(!r.ok)throw new Error(await r.text());return r.json()}
export const getHealth=()=>req("/health");export const getDemo=()=>req("/demo");export const getAnalytics=()=>req("/analytics/summary");
export const startNegotiation=()=>req("/negotiations/start",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});
export const runNegotiation=(id:string)=>req(`/negotiations/${id}/run`,{method:"POST"});
export const approve=(id:string)=>req(`/transactions/${id}/approve`,{method:"POST"});
