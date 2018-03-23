d = [[380   1   1   1   1   0]
 [  0 387   3   0   0   0]
 [  0   4 404   0   0   3]
 [  0   0   0 328   0   0]
 [  0   0   0   0 400   0]
 [  0   0   0   1   0 369]];

score = sum(diag(d))/sum(sum(d));

d = d/max(max(d))*100;

h = heatmap(d);
title('Seat Neuron Classification Accuracy')
xlabel('Predicted Class Accuracy/%')
ylabel('True Class Accuracy/%')
colorbar('off')