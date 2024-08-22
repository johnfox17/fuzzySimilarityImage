clear all;
close all;

addpath('../data/simData/')

fuzzySimilarityImage_cameraman512x512 = table2array(readtable('../data/output/fuzzySimilarityImage_cameraman512x512.csv'));
figure; imagesc(fuzzySimilarityImage_cameraman512x512)
title('Fuzzy Similarity Image Cameraman 512X512')
colormap gray
colorbar
clim([0, 0.52]);

fuzzySimilarityImage_lena512x512 = table2array(readtable('../data/output/fuzzySimilarityImage_lena512x512.csv'));
figure; imagesc(fuzzySimilarityImage_lena512x512)
title('Fuzzy Similarity Image Lena 512X512')
colormap gray
colorbar
clim([0, 0.52]);