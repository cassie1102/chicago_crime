echo off
title Updated chicaho crime data and runs new model/visuals
:: Runs all py files to clean and organize updated data

echo --------------------
echo RUNNING DATA UPDATER
echo --------------------

cd ./etl
call update_data.bat

echo ------------------------------------------------------------
echo DATA SUCCESSFULLY PULLED, FITTING MODEL AND PRINTING VISUALS
echo ------------------------------------------------------------

cd ../model
call get_preds_and_visuals.bat

echo --------------------
echo SYSTEM FULLY UPDATED
echo --------------------