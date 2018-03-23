modeldata = h5read('model.h5', '/dense_1/dense_1/kernel:0');

modeldata = modeldata.^2;

utilz = mean(modeldata);

stem(utilz)

grid on
grid minor
title('Input Neuron Weight Analysis')
xlabel('Neuron Index')
ylabel('Squared Mean Weight')