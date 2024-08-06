#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LENGTH 1024

void scale_coordinate(char *line, float scale_factor) {
    char buffer[MAX_LINE_LENGTH];
    char *ptr = line;
    char *start;
    while ((start = strpbrk(ptr, "XY")) != NULL) {
        // Find the coordinate value after 'X' or 'Y'
        ptr = start + 1;
        // Extract the coordinate value
        float value = strtof(ptr, &ptr);
        // Scale the value
        value *= scale_factor;
        // Format the scaled value
        snprintf(buffer, sizeof(buffer), "%c%.3f", start[0], value);
        // Replace the old value with the new scaled value
        memmove(start + strlen(buffer), ptr, strlen(ptr) + 1);
        memcpy(start, buffer, strlen(buffer));
        ptr = start + strlen(buffer);
    }
}

void scale_gcode(const char *input_filename, const char *output_filename, float scale_factor) {
    FILE *input_file = fopen(input_filename, "r");
    if (input_file == NULL) {
        perror("Error opening input file");
        exit(EXIT_FAILURE);
    }

    FILE *output_file = fopen(output_filename, "w");
    if (output_file == NULL) {
        perror("Error opening output file");
        fclose(input_file);
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), input_file)) {
        // Find the comment character ';' and terminate the line there
        char *comment_start = strchr(line, ';');
        if (comment_start != NULL) {
            *comment_start = '\0'; // Terminate the line before the comment
        }
        // Scale coordinates in each line
        scale_coordinate(line, scale_factor);
        // Write the modified line to the output file
        fputs(line, output_file);
    }

    fclose(input_file);
    fclose(output_file);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <input_file> <output_file> <scale_factor>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *input_filename = argv[1];
    const char *output_filename = argv[2];
    float scale_factor = strtof(argv[3], NULL);

    if (scale_factor <= 0) {
        fprintf(stderr, "Scale factor must be positive.\n");
        return EXIT_FAILURE;
    }

    scale_gcode(input_filename, output_filename, scale_factor);

    return EXIT_SUCCESS;
}
