echo "Compiling IC_generator_sod.cpp"
g++ -o IC_generator_sod IC_generator_sod.cpp
echo ""

echo "Running IC_generator_sod"
./IC_generator_sod
echo ""

echo "Calculating density with PkDGrav3"
cd ../../../pkdgrav3/build/
make
cd ../..
../../../pkdgrav3/build/pkdgrav3 -n0 sod_n0_left.par
../../../pkdgrav3/build/pkdgrav3 -n0 sod_n0_right.par
echo ""

echo "Adjusting temperature to move particles to the same isotrope"
python3 ../../scripts/adjust_isentrope.py sod_n0_left.00000 1.4
python3 ../../scripts/adjust_isentrope.py sod_n0_right.00000 1.4
echo ""

echo "Compiling txt2tipsy.cpp"
g++ -o txt2tipsy ../../scripts/txt2tipsy.cpp
echo ""

echo "Converting to tipsy format"
./txt2tipsy sod_n0_left.00000_adjusted_isentrope
./txt2tipsy sod_n0_right.00000_adjusted_isentrope
echo ""
echo "moving temporary files to temporary folder"
mkdir temporary
mv ic_sod_grid_left_256_32_32.tipsy sod_n0_left.00000 sod_n0_left.00000_adjusted_isentrope.txt temporary
mv ic_sod_grid_right_128_16_16.tipsy sod_n0_right.00000 sod_n0_right.00000_adjusted_isentrope.txt temporary

echo "Moving files"
mv sod_n0_left.00000_adjusted_isentrope.tipsy ../relax/sod_ic_grid_isentrope_left.tipsy
mv sod_n0_right.00000_adjusted_isentrope.tipsy ../relax/sod_ic_grid_isentrope_right.tipsy
cp sod_ic_grid_isentrope_left.tipsy ~/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/
cp sod_ic_grid_isentrope_right.tipsy ~/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/