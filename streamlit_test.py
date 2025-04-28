import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Carvago Chat", layout="wide")
st.title("🚗 Carvago Demo with LiveChat")

livechat_html = """
<!DOCTYPE html>
<html>
  <head>
    <style>
      body { margin: 0; padding: 0; }
    </style>
    <!-- LiveChat loader script with custom variables -->
    <script>
      // Define car data
      const car = {
        id: "8473",
        title: "Škoda Octavia III 1.6 TDI",
        price: "215 000 Kč",
        mileage: "148 000 km"
      };
      
      // Configure LiveChat with custom variables
      window.__lc = window.__lc || {};
      window.__lc.license = 19140581;
      window.__lc.group = 0; // Default group
      
      // Set custom variables as visitor data
      window.__lc.visitor = {
        name: 'Visitor',
        email: 'visitor@example.com',
        car_id: car.id,
        car_title: car.title,
        price: car.price,
        mileage: car.mileage
      };
      
      // Delay LiveChat initialization to ensure variables are set
      window.__lc.asyncInit = true;
      
      // Load the LiveChat tracking script
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
        n.LiveChatWidget = n.LiveChatWidget || e;
      })(window, document, [].slice);
      
      // Initialize LiveChat after a short delay
      setTimeout(function() {
        if (window.LiveChatWidget) {
          window.LiveChatWidget.init();
          console.log("LiveChat initialized with delay");
        }
      }, 1000);
    </script>

    <!-- Additional script to set session variables after widget loads -->
    <script>
      document.addEventListener("DOMContentLoaded", function() {
        // Poll until LiveChat is fully loaded
        const checkInterval = setInterval(function() {
          if (window.LiveChatWidget && typeof window.LiveChatWidget.call === 'function') {
            clearInterval(checkInterval);
            
            // Set session variables explicitly
            window.LiveChatWidget.call("set_session_variables", [
              { name: "car_id", value: car.id },
              { name: "car_title", value: car.title },
              { name: "price", value: car.price },
              { name: "mileage", value: car.mileage }
            ]);
            
            // Also try setting custom variables
            window.LiveChatWidget.call("update_custom_variables", [
              { name: "car_id", value: car.id },
              { name: "car_title", value: car.title },
              { name: "price", value: car.price },
              { name: "mileage", value: car.mileage }
            ]);
            
            console.log("LiveChat session variables set successfully");
          }
        }, 500);
      });
    </script>
  </head>
  <body>
    <!-- Empty div for LiveChat to attach to -->
    <div id="livechat-container"></div>
    
    <!-- Debug information -->
    <div id="debug" style="display:none; padding: 10px; background: #f0f0f0; margin-top: 20px; font-family: monospace;">
      <h3>Debug Info:</h3>
      <div id="debug-output"></div>
    </div>
    
    <script>
      // Add debug functionality
      function addDebugMessage(msg) {
        const debugOutput = document.getElementById('debug-output');
        const msgElement = document.createElement('p');
        msgElement.textContent = new Date().toISOString() + ': ' + msg;
        debugOutput.appendChild(msgElement);
        document.getElementById('debug').style.display = 'block';
      }
      
      // Monitor LiveChat initialization
      const lcCheckInterval = setInterval(function() {
        if (window.LiveChatWidget) {
          addDebugMessage("LiveChatWidget object exists");
          if (typeof window.LiveChatWidget.call === 'function') {
            addDebugMessage("LiveChatWidget.call is available");
            clearInterval(lcCheckInterval);
          }
        }
      }, 1000);
    </script>
  </body>
</html>
"""

# Render the HTML with increased height to ensure the chat widget is fully visible
components.html(livechat_html, height=800)

# Add some additional information below the chat
st.markdown("---")
st.subheader("Car Details")
st.write("ID: 8473")
st.write("Model: Škoda Octavia III 1.6 TDI")
st.write("Price: 215 000 Kč")
st.write("Mileage: 148 000 km")

# Add a button to check LiveChat status
if st.button("Check LiveChat Status"):
    st.code("""
    To check if LiveChat is working properly:
    1. Open browser developer tools (F12)
    2. Go to the Console tab
    3. Look for messages about LiveChat initialization
    4. Check Network tab for requests to livechatinc.com
    """)