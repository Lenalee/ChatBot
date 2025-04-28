import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Carvago Chat", layout="wide")
st.title("🚗 Carvago Demo with LiveChat")

livechat_html = """
<!DOCTYPE html>
<html>
  <head>
    <script>
      window.__lc = window.__lc || {};
      window.__lc.license = 19140581;  // ← your actual LiveChat license

      (function(n,t,c){
        function i(n){ return e._h ? e._h.apply(null,n) : e._q.push(n) }
        var e = {
          _q: [], _h: null, _v:"2.0",
          on:    function(){ i(["on",   c.call(arguments)]) },
          once:  function(){ i(["once", c.call(arguments)]) },
          off:   function(){ i(["off",  c.call(arguments)]) },
          get:   function(){ if(!e._h) throw new Error("[LC] No getters before load."); return i(["get", c.call(arguments)]) },
          call:  function(){ i(["call", c.call(arguments)]) },
          init:  function(){
            var s = t.createElement("script");
            s.async = true;
            s.type  = "text/javascript";
            s.src   = "https://cdn.livechatinc.com/tracking.js";
            t.head.appendChild(s);
          }
        };
        if (!n.__lc.asyncInit) e.init();
        n.LiveChatWidget = n.LiveChatWidget || e;
      })(window, document, [].slice);
    </script>
  </head>
  <body></body>
</html>
"""

# The height must be enough for the widget overlay to appear.
components.html(livechat_html, height=600)