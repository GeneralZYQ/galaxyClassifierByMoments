#include "maxtree.h"

#include <assert.h>
#include <math.h>
#include <time.h>
#include <stdio.h>

#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

#define MT_INDEX_OF(PIXEL) ((PIXEL).location.y * mt->img.width + \
  (PIXEL).location.x)

#define STR_LEN 10

const int mt_conn_12[MT_CONN_12_HEIGHT * MT_CONN_12_WIDTH] =
{
  0, 0, 1, 0, 0,
  0, 1, 1, 1, 0,
  1, 1, 0, 1, 1,
  0, 1, 1, 1, 0,
  0, 0, 1, 0, 0
};

const int mt_conn_8[MT_CONN_8_HEIGHT * MT_CONN_8_WIDTH] =
{
  1, 1, 1,
  1, 0, 1,
  1, 1, 1,
};

const int mt_conn_4[MT_CONN_4_HEIGHT * MT_CONN_4_WIDTH] =
{
  0, 1, 0,
  1, 0, 1,
  0, 1, 0,
};

float calculateMpq (int pixels[], int p, int q, mt_data *mt, int imageWidth, int NIndicesCount) {

    float mpq = 0.0;


    for (int i = 0; i < NIndicesCount; ++i) {
        int value = pixels[i];
        int xc = value % imageWidth;
        int yc = value / imageWidth;
        PIXEL_TYPE imgvalue = mt->img.data[value];
        PIXEL_TYPE mid = pow(xc, p) * pow(yc, q) * imgvalue;
        mpq += mid;
    }

    return mpq;
}

float calculateMiupq(int pixels[], int p, int q, mt_data *mt, int imageWidth, int NIndicesCount) {
    float m10 = calculateMpq(pixels, 1, 0, mt, imageWidth, NIndicesCount);
    float m01 = calculateMpq(pixels, 0, 1, mt, imageWidth, NIndicesCount);
    float m00 = calculateMpq(pixels, 0, 0, mt, imageWidth, NIndicesCount);

    float xcentral = m10 / m00;
    float ycentral = m01 / m00;

    float miupq = 0.0;
    for (int i = 0; i < NIndicesCount; ++i) {
        int xc = pixels[i] % imageWidth;
        int yc = pixels[i] % imageWidth;
        miupq += pow(xc - xcentral, p) * pow(yc - ycentral, q) * mt->img.data[pixels[i]];
    }

    return miupq;
}
//
float calculateItaij (int pixels[], int i, int j, mt_data *mt, int imageWidth, int NIndicesCount) {
    float miuij = calculateMiupq(pixels, i, j, mt, imageWidth, NIndicesCount);
    float miu00 = calculateMiupq(pixels, 0, 0, mt, imageWidth, NIndicesCount);
    float itaij = miuij / pow(miu00, (1 + (i + j) / 2.0));
    return itaij;
}
//
float calculateM1 (int *pixelsp,  mt_data *mt, int imageWidth, int NIndicesCount) {

    float ita20 = calculateItaij(pixelsp, 2, 0, mt, imageWidth, NIndicesCount);
    float ita02 = calculateItaij(pixelsp, 0, 2, mt, imageWidth, NIndicesCount);
    return  ita02 + ita20;
}

float calculateM2(int pixelsp[], mt_data *mt, int imageWidth, int NIndicesCount) {
    float ita11 = calculateItaij(pixelsp, 1, 1, mt, imageWidth, NIndicesCount);
    float ita20 = calculateItaij(pixelsp, 2, 0, mt, imageWidth, NIndicesCount);
    float ita02 = calculateItaij(pixelsp, 0, 2, mt, imageWidth, NIndicesCount);
    return  pow(ita20 - ita02, 2) + 4 * pow(ita11, 2);
}

float calculateM3 (int pixelsp[], mt_data *mt, int imageWidth, int imageHeight) {
    float ita30 = calculateItaij(pixelsp, 3, 0, mt, imageWidth, imageHeight);
    float ita12 = calculateItaij(pixelsp, 1, 2, mt, imageWidth, imageHeight);
    float ita21 = calculateItaij(pixelsp, 2, 1, mt, imageWidth, imageHeight);
    float ita03 = calculateItaij(pixelsp, 0, 3, mt, imageWidth, imageHeight);
    return pow(ita30 - 3 * ita12, 2) + pow(3 * ita21 - ita03 , 2);
}

float calculateM4 (int pixelsp[], mt_data *mt, int imageWidth, int imageHeight) {
    float ita30 = calculateItaij(pixelsp, 3, 0, mt, imageWidth, imageHeight);
    float ita12 = calculateItaij(pixelsp, 1, 2, mt, imageWidth, imageHeight);
    float ita21 = calculateItaij(pixelsp, 2, 1, mt, imageWidth, imageHeight);
    float ita03 = calculateItaij(pixelsp, 0, 3, mt, imageWidth, imageHeight);
    return pow(ita30 + ita12, 2) + pow(ita21 + ita03, 2);
}

float calculateM5 (int pixelsp[], mt_data *mt, int imageWidth, int imageHeight) {
    float ita30 = calculateItaij(pixelsp, 3, 0, mt, imageWidth, imageHeight);
    float ita12 = calculateItaij(pixelsp, 1, 2, mt, imageWidth, imageHeight);
    float ita21 = calculateItaij(pixelsp, 2, 1, mt, imageWidth, imageHeight);
    float ita03 = calculateItaij(pixelsp, 0, 3, mt, imageWidth, imageHeight);

    return (ita30 - 3 * ita12) * (ita30 + ita12) * (pow(ita30 + ita12, 2) - 3 * pow(ita21 + ita03, 2)) + (3 * ita21 - ita03) * (ita21 + ita03) * (3 * pow(ita30 + ita12 , 2) - pow(ita21 + ita03, 2));
}

float calculateM6 (int pixelsp[], mt_data *mt, int imageWidth, int imageHeight) {
    float ita20 = calculateItaij(pixelsp, 2, 0, mt, imageWidth, imageHeight);
    float ita02 = calculateItaij(pixelsp, 0, 2, mt, imageWidth, imageHeight);
    float ita30 = calculateItaij(pixelsp, 3, 0, mt, imageWidth, imageHeight);
    float ita12 = calculateItaij(pixelsp, 1, 2, mt, imageWidth, imageHeight);
    float ita21 = calculateItaij(pixelsp, 2, 1, mt, imageWidth, imageHeight);
    float ita03 = calculateItaij(pixelsp, 0, 3, mt, imageWidth, imageHeight);
    float ita11 = calculateItaij(pixelsp, 1, 1, mt, imageWidth, imageHeight);
    return (ita20 - ita02) * (pow(ita30 + ita12, 2) - pow(ita21 + ita03, 2)) + 4 * ita11 * (ita30 + ita12) * (ita21 + ita03);
}

float calculateM7 (int pixelsp[], mt_data *mt, int imageWidth, int imageHeight) {
    float ita21 = calculateItaij(pixelsp, 2, 1, mt, imageWidth, imageHeight);
    float ita03 = calculateItaij(pixelsp, 0, 3, mt, imageWidth, imageHeight);
    float ita12 = calculateItaij(pixelsp, 1, 2, mt, imageWidth, imageHeight);
    float ita30 = calculateItaij(pixelsp, 3, 0, mt, imageWidth, imageHeight);

    return (3 * ita21 - ita03) * (ita30 + ita12) * (pow(ita30 + ita12, 2) - 3 * pow(ita21 + ita03, 2)) - (ita30 - 3 * ita12) * (ita21 + ita03) * (3 * pow(ita30 + ita12, 2) - pow(ita21 + ita03, 2));
}

char *GenerateStr()
{
    char str[STR_LEN + 1] = {0};
    int i,flag;

    srand(time(NULL));
    for(i = 0; i < STR_LEN; i ++)
    {
        flag = rand()%3;
        switch(flag)
        {
            case 0:
                str[i] = rand()%26 + 'a';
                break;
            case 1:
                str[i] = rand()%26 + 'A';
                break;
            case 2:
                str[i] = rand()%10 + '0';
                break;
        }
    }
    // printf("%s\n", str);

    return str;
}

mt_pixel mt_starting_pixel(mt_data* mt)
{
  // Find the minimum pixel value in the image
  SHORT_TYPE y;
  SHORT_TYPE x;

  mt_pixel pixel;
  pixel.location.x = 0;
  pixel.location.y = 0;

  pixel.value = mt->img.data[0];

  // iterate over image pixels
  for (y = 0; y != mt->img.height; ++y)
  {
    for (x = 0; x != mt->img.width; ++x)
    {
	  // Convert from x,y coordinates to an array index
      INT_TYPE index = y * mt->img.width + x;

      // If the pixel is less than the current minimum, update the minimum
      if (mt->img.data[index] < pixel.value)
      {
        pixel.value = mt->img.data[index];
        pixel.location.x = x;
        pixel.location.y = y;

      }
    }
  }

  return pixel;
}

static void mt_init_nodes(mt_data* mt)
{
  // Initialise the nodes of the maxtree
  INT_TYPE i;

  // Set all parents as unassigned, and all areas as 1
  for (i = 0; i != mt->img.size; ++i)
  {
    mt->nodes[i].parent = MT_UNASSIGNED;
    mt->nodes[i].area = 1;
  }
}

static void mt_init_node_indexes(mt_data *mt) {
    // Initialise the node_indexes of the maxtree
    INT_TYPE i;

    for (i = 0; i != mt->img.size; ++i) {
        mt->nodeIndexes[i].index = i;

        char str[17];
        sprintf(str, "%d", i);
        mt->nodeIndexes[i].indexes = str;
    }
}

static void mt_init_node_moments (mt_data *mt) {
    INT_TYPE i;

    for (i = 0; i != mt->img.size; ++i) {
        mt->moments[i].index = i;

        mt->moments[i].value = 0.0;
        mt->moments[i].moment1 = 0.0;
        mt->moments[i].moment2 = 0.0;
        mt->moments[i].moment3 = 0.0;
        mt->moments[i].moment4 = 0.0;
        mt->moments[i].moment5 = 0.0;
        mt->moments[i].moment6 = 0.0;
        mt->moments[i].moment7 = 0.0;

    }
}

static void mt_calculate_moments (mt_data *mt) {
    INT_TYPE i;
    for (i = 0; i != mt->img.size; ++i) {
        mt_node mtNode = mt->nodes[i];

        if (1 % 50 == 0)
        {
          printf("The current index is %d\n", i);
        }
        if (mtNode.area > 1) {
            mt_node_indexes mtNodeIndexes = mt->nodeIndexes[i];
            mt_node_moments mtNodeMoments = mt->moments[i];
            char indexes[1000*1000*7];

//            printf("hte indexes is %s", indexes);
            strcpy(indexes, mtNodeIndexes.indexes);

            int (*rawpixels)=(int (*))malloc(sizeof(int)*(1000*1000));

            int TotalCount = 0;
            char *p = strtok(indexes,",");

            while (p != NULL) {

                int midInd = atoi(p);
                rawpixels[TotalCount++] = midInd;
                p = strtok(NULL,",");
            }

            int (*pixels)=(int (*))malloc(sizeof(int)*TotalCount);

            for (int j = 0; j < TotalCount; ++j) {
                int jva = rawpixels[j];
                pixels[j] = rawpixels[j];
            }

            PIXEL_TYPE m1 = calculateM1(pixels, mt, mt->img.width, TotalCount);
            PIXEL_TYPE m2 = calculateM2(pixels, mt, mt->img.width, TotalCount);
            PIXEL_TYPE m3 = calculateM3(pixels, mt, mt->img.width, TotalCount);
            PIXEL_TYPE m4 = calculateM4(pixels, mt, mt->img.width, TotalCount);
            PIXEL_TYPE m5 = calculateM5(pixels, mt, mt->img.width, TotalCount);
            PIXEL_TYPE m6 = calculateM6(pixels, mt, mt->img.width, TotalCount);
            PIXEL_TYPE m7 = calculateM7(pixels, mt, mt->img.width, TotalCount);

            mt->moments[i].value = mt->img.data[i];
            mt->moments[i].moment1 = m1;
            mt->moments[i].moment2 = m2;
            mt->moments[i].moment3 = m3;
            mt->moments[i].moment4 = m4;
            mt->moments[i].moment5 = m5;
            mt->moments[i].moment6 = m6;
            mt->moments[i].moment7 = m7;

            // printf("I am caculatedd! with index %d and the moment1 is %f\n ", mtNodeMoments.index, mtNodeMoments.moment1);


            free(rawpixels);
            free(pixels);

        }
    }
}

static void mt_calculate_local_spectrum(mt_data *mt) {

    FILE *wfp = NULL;
    char *result_file_path = (char*)malloc(sizeof(char)*512);

    if(result_file_path == NULL){
        printf("allocate memory for file path failed.\n");
    }

    memset(result_file_path, 0, sizeof(char)*512);
    char *finalname = (char*)malloc(sizeof(char)*512);
    sprintf(finalname, "%d_%d_%d_%s_localSpectrum.csv", mt->img.size, mt->img.width, mt->img.height, GenerateStr());

    sprintf(result_file_path, "%s/%s", "/Volumes/DISK1/spectrums/7MomentsSpirals", finalname);

    wfp = fopen(result_file_path, "a");
    if(NULL == wfp)
    {
        return; //
    }

    printf("Start calculating local spectrums!\n", );

    for (int i = 0; i < mt->img.size; ++i) {
        if (mt->nodes[i].area > 1) {
            int parent = mt->nodes[i].parent;
            if (parent == MT_NO_PARENT || parent == 0) {
                continue;
            }

            int currentArea = mt->nodes[i].area;
            PIXEL_TYPE currentValue =  mt->moments[i].value;
            float currentM1 = mt->moments[i].moment1;
            float currentM2 = mt->moments[i].moment2;
            float currentM3 = mt->moments[i].moment3;
            float currentM4 = mt->moments[i].moment4;
            float currentM5 = mt->moments[i].moment5;
            float currentM6 = mt->moments[i].moment6;
            float currentM7 = mt->moments[i].moment7;


            PIXEL_TYPE fatherValue =  mt->moments[parent].value;
            float fatherM1 = mt->moments[parent].moment1;
            float fatherM2 = mt->moments[parent].moment2;
            float fatherM3 = mt->moments[parent].moment3;
            float fatherM4 = mt->moments[parent].moment4;
            float fatherM5 = mt->moments[parent].moment5;
            float fatherM6 = mt->moments[parent].moment6;
            float fatherM7 = mt->moments[parent].moment7;

            float deltaValue = currentValue - fatherValue;

            float spectrums[9] = {currentArea, deltaValue, currentM1 - fatherM1, currentM2 - fatherM2, currentM3 - fatherM3, currentM4 - fatherM4, currentM5 - fatherM5, currentM6 - fatherM6, currentM7 - fatherM7};


            for (int j = 0; j < 9; ++j) {
                if (j ==  8) {
                    fprintf(wfp, "%f", spectrums[j]);
                } else {
                    fprintf(wfp, "%f,", spectrums[j]);
                }
            }
            fprintf(wfp, "\n");
        }
    }

    fprintf(wfp, "\n");
//
    close(wfp);
}

static int mt_queue_neighbour(mt_data* mt, PIXEL_TYPE val,
  SHORT_TYPE x, SHORT_TYPE y)
{
  // Add a pixel to the queue for processing

  //Create a pixel and set its location
  mt_pixel neighbour;
  neighbour.location.x = x;
  neighbour.location.y = y;

  // Convert from x,y coordinates to an array index
  INT_TYPE neighbour_index = MT_INDEX_OF(neighbour);
  // Get a pointer to the neighbour
  mt_node *neighbour_node = mt->nodes + neighbour_index;

  // If the neighbour has not already been processed, add it to the queue
  if (neighbour_node->parent == MT_UNASSIGNED)
  {
    neighbour.value = mt->img.data[neighbour_index];
    neighbour_node->parent = MT_IN_QUEUE;
    mt_heap_insert(&mt->heap, &neighbour);

    // If the neighbour has a higher value than the current node, return 1
    if (neighbour.value > val)
    {
      return 1;
    }
  }

  return 0;
}

static void mt_queue_neighbours(mt_data* mt,
  mt_pixel* pixel)
{
  // Seems to be limiting conn values within image coordinates

  // Radius is half size of connectivity
  INT_TYPE radius_y = mt->connectivity.height / 2;
  INT_TYPE radius_x = mt->connectivity.width / 2;

  // If pixel's x is less than radius, conn = the difference
  INT_TYPE conn_x_min = 0;
  if (pixel->location.x < radius_x)
    conn_x_min = radius_x - pixel->location.x;

  // Ditto for y
  INT_TYPE conn_y_min = 0;
  if (pixel->location.y < radius_y)
    conn_y_min = radius_y - pixel->location.y;

  // If pixel's x + radius > image width, conn = radius + width - location - 1
  INT_TYPE conn_x_max = 2 * radius_x;
  if (pixel->location.x + radius_x >= mt->img.width)
    conn_x_max = radius_x + mt->img.width - pixel->location.x - 1;

  INT_TYPE conn_y_max = 2 * radius_y;
  if (pixel->location.y + radius_y >= mt->img.height)
    conn_y_max = radius_y + mt->img.height - pixel->location.y - 1;

  INT_TYPE conn_y;
  // Conn coordinates refer to position with connectivity grid
  for (conn_y = conn_y_min; conn_y <= conn_y_max; ++conn_y)
  {
    INT_TYPE conn_x;
    for (conn_x = conn_x_min; conn_x <= conn_x_max; ++conn_x)
    {
	  // Skip iteration if 0 in connectivity grid
      if (mt->connectivity.
        neighbors[conn_y * mt->connectivity.width + conn_x] == 0)
      {
        continue;
      }

      // Try to queue neighbour at x = x-rad+conn
      // If successfully queued and value higher than current,
      // break out of function
      if (mt_queue_neighbour(mt, pixel->value,
        pixel->location.x - radius_x + conn_x,
        pixel->location.y - radius_y + conn_y))
      {
        return;
      }
    }
  }
}

static void mt_merge_nodes(mt_data* mt,
  INT_TYPE merge_to_idx,
  INT_TYPE merge_from_idx)
{
  // Merge two nodes

  mt_node *merge_to = mt->nodes + merge_to_idx;
  mt_node_attributes *merge_to_attr = mt->nodes_attributes +
    merge_to_idx;

  mt_node *merge_from = mt->nodes + merge_from_idx;
  mt_node_attributes *merge_from_attr = mt->nodes_attributes +
    merge_from_idx;

  merge_to->area += merge_from->area;

  FLOAT_TYPE delta = mt->img.data[merge_from_idx] -
    mt->img.data[merge_to_idx];

  merge_from_attr->power += delta *
    (2 * merge_from_attr->volume + delta * merge_from->area);
  merge_to_attr->power += merge_from_attr->power;

  merge_from_attr->volume += delta * merge_from->area;
  merge_to_attr->volume += merge_from_attr->volume;
}

static void mt_descend(mt_data* mt, mt_pixel *next_pixel)
{
  mt_pixel old_top = *mt_stack_remove(&mt->stack);
  INT_TYPE old_top_index = MT_INDEX_OF(old_top);


  mt_pixel* stack_top = MT_STACK_TOP(&mt->stack);

  if (stack_top->value < next_pixel->value)
  {
    mt_stack_insert(&mt->stack, next_pixel);
  }

  stack_top = MT_STACK_TOP(&mt->stack);
  INT_TYPE stack_top_index = MT_INDEX_OF(*stack_top);

  mt->nodes[old_top_index].parent = stack_top_index;

  //This is the start====

  // char *currentIndexes = mt->nodeIndexes[stack_top_index].indexes;
  // char finalCurrentIndex[1000*1000*7];
  // sprintf(finalCurrentIndex, "%s", currentIndexes);
  // char *toAddIndexes = mt->nodeIndexes[old_top_index].indexes;
  // strcat(finalCurrentIndex, ",");
  // strcat(finalCurrentIndex, toAddIndexes);
  // mt->nodeIndexes[stack_top_index].indexes = finalCurrentIndex;

    char *currentIndexes = mt->nodeIndexes[stack_top_index].indexes;
    char *finalCurrentIndex = (char*) malloc(1000000*7* sizeof(char));
    sprintf(finalCurrentIndex, "%s", currentIndexes);
    char *toAddIndexes = mt->nodeIndexes[old_top_index].indexes;
    strcat(finalCurrentIndex, ",");
    strcat(finalCurrentIndex, toAddIndexes);
    mt->nodeIndexes[stack_top_index].indexes = strdup(finalCurrentIndex) ;
    free(finalCurrentIndex);

  //This is the end====


  mt_merge_nodes(mt, stack_top_index, old_top_index);
}

static void mt_remaining_stack(mt_data* mt)
{
  while (MT_STACK_SIZE(&mt->stack) > 1)
  {
    mt_pixel old_top = *mt_stack_remove(&mt->stack);
    INT_TYPE old_top_index = MT_INDEX_OF(old_top);

    mt_pixel* stack_top = MT_STACK_TOP(&mt->stack);
    INT_TYPE stack_top_index = MT_INDEX_OF(*stack_top);

    mt->nodes[old_top_index].parent = stack_top_index;
    mt_merge_nodes(mt, stack_top_index, old_top_index);
  }
}

void mt_flood(mt_data* mt)
{
  assert(mt->connectivity.height > 0);
  assert(mt->connectivity.height % 2 == 1);
  assert(mt->connectivity.width > 0);
  assert(mt->connectivity.width % 2 == 1);

  if (mt->verbosity_level)
  {
    int num_neighbors = 0;
    int i;
    for (i = 0; i != mt->connectivity.height; ++i)
    {
      int j;
      for (j = 0; j != mt->connectivity.width; ++j)
      {
        if (mt->connectivity.neighbors[i * mt->connectivity.width + j])
        {
          ++num_neighbors;
        }
      }
    }

    printf("%d neighbors connectivity.\n", num_neighbors);
  }


  mt_pixel next_pixel = mt_starting_pixel(mt);
  INT_TYPE next_index = MT_INDEX_OF(next_pixel);
  mt->root = mt->nodes + next_index;
  mt->nodes[next_index].parent = MT_NO_PARENT;
  mt_heap_insert(&mt->heap, &next_pixel);
  mt_stack_insert(&mt->stack, &next_pixel);

  while (MT_HEAP_NOT_EMPTY(&mt->heap))
  {
    mt_pixel pixel = next_pixel; // to construct
    INT_TYPE index = next_index;

    mt_queue_neighbours(mt, &pixel);

    next_pixel = *MT_HEAP_TOP(&mt->heap);
    next_index = MT_INDEX_OF(next_pixel);
    // printf("The pixel value is %f\n", next_pixel.value);

    if (next_pixel.value > pixel.value)
    {
      // Higher level
      // printf("heigher : the pixel value is %f\n", next_pixel.value);
      mt_stack_insert(&mt->stack, &next_pixel); // It is higher, we will process it later.
      continue;
    }

    pixel = *mt_heap_remove(&mt->heap);
    index = MT_INDEX_OF(pixel);
    mt_pixel *stack_top = MT_STACK_TOP(&mt->stack);
    INT_TYPE stack_top_index = MT_INDEX_OF(*stack_top);

    if (index != stack_top_index)
    {
      mt->nodes[index].parent = stack_top_index;
      ++mt->nodes[stack_top_index].area;

      //This is the start ====

      // char *currentIndexes = mt->nodeIndexes[stack_top_index].indexes;
      // char finalCurrentIndex[1000*1000*7];
      // char toAddIndex[17];
      // sprintf(toAddIndex, "%d", index);
      // sprintf(finalCurrentIndex, "%s", currentIndexes);
      // strcat(finalCurrentIndex, ",");
      // strcat(finalCurrentIndex, toAddIndex);
      // mt->nodeIndexes[stack_top_index].indexes = finalCurrentIndex;

      char *currentIndexes = mt->nodeIndexes[stack_top_index].indexes;
      char *finalCurrentIndex = (char*) malloc(1000000*7* sizeof(char));
      char toAddIndex[17];
      sprintf(toAddIndex, "%d", index);
      sprintf(finalCurrentIndex, "%s", currentIndexes);
      strcat(finalCurrentIndex, ",");
      strcat(finalCurrentIndex, toAddIndex);
      mt->nodeIndexes[stack_top_index].indexes = strdup(finalCurrentIndex);
      free(finalCurrentIndex);

      // This is the end ===
    }

    if (MT_HEAP_EMPTY(&mt->heap))
    {
      break;
    }

    next_pixel = *MT_HEAP_TOP(&mt->heap);
    next_index = MT_INDEX_OF(next_pixel);

    if (next_pixel.value < pixel.value)
    {
      // Lower level

      mt_descend(mt, &next_pixel);
    }
  }

  mt_remaining_stack(mt);
  mt_calculate_moments(mt);

  mt_calculate_local_spectrum(mt);

  mt_stack_free_entries(&mt->stack);
  mt_heap_free_entries(&mt->heap);

  
}

void mt_init(mt_data* mt, const image* img)
{
  mt->img = *img;

  mt->nodes = safe_malloc(mt->img.size * sizeof(mt_node));
  mt->nodes_attributes = safe_calloc(mt->img.size,
    sizeof(mt_node_attributes));


  printf("The size of raw indexes is %lu\n", sizeof(mt_node_indexes));

  mt->nodeIndexes = safe_malloc(mt->img.size * sizeof(mt_node_indexes));
  mt->moments = safe_malloc(mt->img.size * sizeof(mt_node_moments));


  mt_stack_alloc_entries(&mt->stack);
  mt_heap_alloc_entries(&mt->heap);

  mt_init_nodes(mt);
  mt_init_node_indexes(mt);
  mt_init_node_moments(mt);

  mt->connectivity.neighbors = mt_conn_4;
  mt->connectivity.width = MT_CONN_4_WIDTH;
  mt->connectivity.height = MT_CONN_4_HEIGHT;

  mt->verbosity_level = 0;
}

void mt_free(mt_data* mt)
{
  // Free the memory occupied by the max tree
  free(mt->nodes);
  free(mt->nodes_attributes);
  // free(mt->moments);
  free(mt->nodeIndexes);

  //memset(mt, 0, sizeof(mt_data));
}

void mt_set_verbosity_level(mt_data* mt, int verbosity_level)
{
  mt->verbosity_level = verbosity_level;
}
