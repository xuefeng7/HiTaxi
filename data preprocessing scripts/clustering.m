% clustering
% using kmeans++, k=30,40,50
[idx,C,sumd,D] = kmeans(points, 50);
[r, ~] = size(points);
map = containers.Map;
for i = 1:r
    cidx = idx(i); %cluster index
    coord = points(i,:);
    centroid = C(cidx,:);
    dist = D(i, cidx);
    if isKey(map,num2str(centroid))
        % add points
        map(num2str(centroid)) = [map(num2str(centroid)); coord];
    else
        % create key and add points
        map(num2str(centroid)) = [coord];
    end
end
output = fopen('points_k=50.txt', 'a');

keySet = keys(map);
[~, l] = size(keySet);

for j = 1:l
    fprintf(output, '%s:\n', keySet{j});
    pts = map(keySet{j});
    [r, ] = size(pts);
    for k = 1:r
        fprintf(output, '%s\n', num2str(pts(k,:)));
    end
end

