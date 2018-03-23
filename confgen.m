d = [[383   0   1   1   2   0]
 [  2 308   4   0   5  57]
 [  1   0 381   0   4   0]
 [  0   0   0 366   0   0]
 [  0   0   6   0 394   3]
 [  0  26   0   0   0 339]];

score = sum(diag(d))/sum(sum(d));

d = d/max(max(d))*100;

h = heatmap(d);
title('Full Neuron Classification Accuracy')
xlabel('Predicted Class Accuracy/%')
ylabel('True Class Accuracy/%')
colorbar('off')