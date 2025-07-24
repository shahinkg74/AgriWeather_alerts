import requests
import tkinter as tk
from tkinter import ttk ,messagebox
from datetime import datetime, timedelta

class AgriWeatherAlert:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent agricultural warning system")
        self.root.geometry("850x650")

        # API SETTING
        self.API_KEY = "your API key"  #PUT YOUR API KEY
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/onecall"

                 # Loading the agricultural cities of Iran
        self.agri_cities = ["esfehan", "ahvaz", "shiraz", "mashhad", "tabriz"]

        # my creative ideas 
        self.crop_types = {
            "wheat": {"min_temp": -5, "max_temp": 35, "rain_needed": 30},
            "barley": {"min_temp": -5, "max_temp": 30, "rain_needed": 25},
            "cotton": {"min_temp": 15, "max_temp": 40, "rain_needed": 50},
            "rice": {"min_temp": 10, "max_temp": 38, "rain_needed": 150}
        }
         
        # creating a user interface
        self.setup_ui()

    def setup_ui(self):
            # Customized user interface for farmers
            main_frame = tk.Frame(self.root, padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)

            header =tk.Label(main_frame, 
                         text="🚜 Agricultural Meteorological Warning System",
                         font=("Arial", 18, "bold"),
                         fg="green")
            header.pack(pady = 10)

            ## Selection controls
            control_frame = tk.Frame(main_frame)
            control_frame.pack(fill=tk.X, pady=10)

            tk.Label(control_frame, text="city:").pack(side=tk.LEFT, padx=5)
            self.city_combo = ttk.Combobox(control_frame, values=self.agri_cities)
            self.city_combo.pack(side=tk.LEFT, padx=5)

            tk.Label(control_frame, text="crop:").pack(side=tk.LEFT, padx=5)
            self.crop_combo = ttk.Combobox(control_frame, values=list(self.crop_types.keys()))
            self.crop_combo.pack(side=tk.LEFT, padx=5)

            #Button
            tk.Button(control_frame, 
                 text=" Receive alerts ",
                 command=self.get_alerts,
                 bg="green",
                 fg="white").pack(side=tk.RIGHT)
            
            #Results display panel
            self.result_frame = tk.LabelFrame(main_frame, 
                                        text="Meteorological advice",
                                        padx=10,
                                        pady=10)
            self.result_frame.pack(fill=tk.BOTH, expand=True)

            self.alert_label = tk.Label(self.result_frame, 
                                  font=("Arial", 12),
                                  justify="left",
                                  wraplength=700)
            self.alert_label.pack(pady=10)
            self.advice_label = tk.Label(self.result_frame,
                                    font=("Arial", 12, "italic"),
                                    fg="blue",
                                    wraplength=700)
            self.advice_label.pack(pady=10)
            
            #Advertising related services (money-making idea)

            service_frame = tk.Frame(main_frame)
            service_frame.pack(fill=tk.X, pady=10)

            tk.Label(service_frame, 
                text="Specialized agricultural advice: 09123456789",
                fg="darkgreen").pack()
            
    def get_alerts(self):
            #Acquiring meteorological data and analysis for agriculture

            city = self.city_combo.get()
            crop = self.crop_combo.get()

            if not city or not crop :
                messagebox.showerror("Please select city and product", "error")
                return
            
            try:
                 # دریافت مختصات جغرافیایی شهر
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.API_KEY}"
                #geo_data = requests.get(geo_url).json()
                geo_response = requests.get(geo_url)

                if geo_response.status_code != 200:
                     messagebox.showerror("خطا", f"خطا در دریافت مختصات: {geo_response.status_code}")
                     return
                
                geo_data = geo_response.json()

                if not geo_data:
                    messagebox.showerror("خطا", "شهر مورد نظر یافت نشد!")
                    return
                lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
                params =  {
                     "lat": lat,
                     "lon": lon,
                     "exclude": "minutely,hourly",
                     "appid": self.API_KEY,
                     "units": "metric",
                     "lang": "fa"
                }

                weather_response = requests.get(self.BASE_URL, params=params)

                if weather_response.status_code != 200:
                      messagebox.showerror("خطا", f"خطا در دریافت داده‌های آب و هوا: {weather_response.status_code}")
                      return
                
                weather_data = weather_response.json()
               # weather_data = requests.get(self.BASE_URL, params=params).json()
                current =  weather_data.get("current", {})
                daily =  weather_data.get("daily", [{}])[0]

                crop_info = self.crop_types.get(crop, {})
                alerts = []
                advice = []

                temp = current.get("temp", 0)
                if temp < crop_info ["min_temp"]:
                    alerts.append(f"⚠️ هشدار یخبندان: دمای {temp}°C برای {crop} خطرناک است")
                    advice.append(f"• محصولات خود را بپوشانید\n• از سیستم گرمایشی استفاده کنید")
                elif temp > crop_info ["max_temp"]:
                    alerts.append(f"⚠️ هشدار گرمای شدید: دمای {temp}°C برای {crop} مضر است")
                    advice.append(f"• آبیاری را افزایش دهید\n• از سایبان استفاده کنید")

                    rain = daily.get("rain", 0)
                    if rain < crop_info ["rain_needed"]* 0.5:
                        alerts.append(f"🚱 هشدار خشکسالی: بارش {rain}mm کم است")
                        advice.append(f"• آبیاری مکمل انجام دهید\n• از سیستم آبیاری قطره‌ای استفاده کنید")    
                    
                    self.alert_label.config(text="\n".join(alerts) if alerts else "✅ شرایط جوی مناسب است")
                    self.advice_label.config(text="\n".join(advice) if advice else "• به برنامه عادی ادامه دهید")
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در دریافت داده‌ها: {str(e)}")

            

                    
            
                
        
def main():
    root = tk.Tk()
    app = AgriWeatherAlert(root)
    root.mainloop() 

if __name__ == "__main__":
     main()
           

                



            



