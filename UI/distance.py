import googlemaps
import math


def convertTo2DArray(listMarker):
    api_key = "AIzaSyCNHayAJYOTf-gi30fTgbA3SEXpjj3LDFM"
    gmaps = googlemaps.Client(key=api_key)

    dis_mat = [[1 for x in range(len(listMarker))] for y in range(len(listMarker))]
    for i in range(len(listMarker)):
        for j in range(len(listMarker)):
            if i == j:
                dis_mat[i][j] = 0
            else:
                #duration = gmaps.distance_matrix(origins=(listMarker[i]['latitude'], listMarker[i]['longitude']),
                                                 #destinations=(listMarker[j]['latitude'], listMarker[j]['longitude']),
                                                 #mode="driving")
                #dis_mat[i][j] = duration['rows'][0]['elements'][0]['duration']['value']
                dis_mat[i][j] = math.sqrt(math.pow(listMarker[i]['latitude'] - listMarker[j]['latitude'], 2)
                                          + math.pow(listMarker[i]['longitude'] - listMarker[j]['longitude'], 2))
            print(dis_mat)
    return dis_mat
