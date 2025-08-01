1. SDK aik frame work hai multi agent bnany ka.
2. Agent Runner ke andar wrap ho kar chal rha hota hai or Agent ke pass LLM hota hai or ye agent ka dimagh hai or
   Agent jo bhi kaam karta hai wo LLM se pochy bagher nahi karta pehly us se pochta hai bad mein karta hai.
3. User ka input RUnner ka zariye Agent ke pass jata hai or agent kya karta hai apni sari cheezen utha kar LLM 
   dey deta hai jese Tool_functions handsoff Agents phir LLM btata hai ke tum konsa tool karo user ke is swal ke mutabik.
4. Kisi bhi LLM ko lgane ke liye 2 cheezen chahiye hoti hain aik 1.(API KEY) or dosri 2.(BaseUrl) wo API Aa kahn 
   se rhi hai.      

5. LiteLLM -> Using any model via LiteLLM
6. install -> uv add "openai-agents[litellm]"   
7. LiteLLM kehta hai ke jo model ham use karenge uski website par jaa kar uski api key create karni paregi.


8. uv add openai-agents + uv add "openai-agents[litellm]"

   jab ham sinple (openai-agents) isntall kar ke Agents create kar ke kaam karty hain or uske bad usi project folder mein ham jab (litellm) ko install kar ke use karty hain to hamen preshani ka smana karna par sakta hai 
   errors bhi aa sakty hain kiyun ke (litellm) walon ne apna sara kaam SDK ke opar bnaya hua hai.

9. uv remove openai-agents
   agr ham simple (openai-agents) waly project folder mein (litellm) ka kaam karna chahty hain to sab se pehly
   us folder mein hamen ye command chlani paregi.