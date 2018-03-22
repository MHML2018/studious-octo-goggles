modeldata = h5read('model.h5', '/dense_1/dense_1/kernel:0');

datam = mean(modeldata);

utilz = datam.^2;

stem(utilz)