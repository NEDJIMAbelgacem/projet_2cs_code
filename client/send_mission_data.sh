python3 fetch_data.py --obd_device /dev/pts/2 --sleep_time 0.5 --nb_data_fetch 5 --vehicle_name $1 --vehicle_matricule $2 > ./session_fetched_data.txt
python3 encrypt_and_send.py
# rm ./session_data.txt
