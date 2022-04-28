# include <stdio.h>
# include <math.h>
# include <ctype.h>
# include <stdlib.h>
# include <string.h>
# define MAXCHAR 128
# define MAXFEATURE 1000
 
char ifilename[MAXCHAR];
char ofilename[MAXCHAR];
char ffilename[MAXCHAR];
char line[MAXCHAR];

FILE *fpin, *fpout, *ffeature;

char tmpchar[MAXCHAR];
char tmpchar1[MAXCHAR];
char tmpchar2[MAXCHAR];
char tmpchar3[MAXCHAR];
char feature[MAXFEATURE][MAXCHAR];
char ftype[MAXFEATURE];
char value[MAXFEATURE][MAXCHAR];
int readfeature = 0;
int delimiter = 1;
int fnum = 0;
int ifield = 1;
 
int  main(int argc, char *argv[]) {
int i,j;
if((argc==2&&(strcmp(argv[1], "-h")==0||strcmp(argv[1], "-H")==0))|| argc!=11 && argc!=9 && argc!=7) {
	printf("Usage: sd_extract_field  -i  sd file name\n");
    	printf("                         -d  delimiter (0 for tab and 1 for ,\n");
    	printf("                         -f  feature file name (if it is not provided, the features in the first entry are used\n"); 
    	printf("                         -o output file name\n");
    	printf("                         -l write fields in the first line: 1-yes (the default), 0-no\n");
    	exit(0);
}
 
for(i=1;i<argc;i+=2) {
    	if(strcmp(argv[i], "-i")==0) {
     		strcpy(ifilename, argv[i+1]);
     		continue;
    	}
    	if(strcmp(argv[i], "-o")==0) {
     		strcpy(ofilename, argv[i+1]);
     		continue;
    	}
    	if(strcmp(argv[i], "-d")==0){ 
		delimiter = atoi(argv[i+1]);
     		continue;
    	}
    	if(strcmp(argv[i], "-f")==0) {
     		strcpy(ffilename, argv[i+1]);
		readfeature = 1;
     		continue;
	}
    	if(strcmp(argv[i], "-l")==0) {
		ifield = atoi(argv[i+1]);
     		continue;
	}
}	
 
if(readfeature == 1)
	if((ffeature=fopen(ffilename,"r"))==NULL) {
		printf("\n Cannot open file %s, exit", ffilename);
     		return 0;
	}
if((fpin=fopen(ifilename,"r"))==NULL) {
  	printf("\n Cannot open file %s, exit", ifilename);
        return 0;
}
if((fpout=fopen(ofilename,"w"))==NULL) {
  	printf("\n Cannot open file %s to write , exit", ofilename);
        return 0;
}
if(ifield != 0 && ifield !=1) ifield = 1;
 
fnum = 0;
if(readfeature == 1) {
	for(;;) {
		if(fgets(line,MAXCHAR,ffeature) ==NULL) break;
		strcpy(tmpchar1, "");
		strcpy(tmpchar2, "");
		tmpchar1[0] = '\0';
		tmpchar2[0] = '\0';
       		sscanf(line, "%s%s", tmpchar1, &tmpchar2); 
		if(strcmp(tmpchar2 , "+") == 0) 
			ftype[fnum] = 1;		
		else
			ftype[fnum] = 0;
		strcpy(tmpchar2, "<");
		strcat(tmpchar2, tmpchar1);
		strcat(tmpchar2, ">");
		strcpy(feature[fnum], tmpchar2);
		fnum++;
	}
	fclose(ffeature);
}
if(readfeature == 0) 
	for(;;) {
		if(fgets(line,MAXCHAR,fpin) ==NULL) break;
		strcpy(tmpchar1, "");
		strcpy(tmpchar2, "");
       		sscanf(line, "%s%s", tmpchar1, tmpchar2);
		if(strcmp(tmpchar1, "$$$$") == 0) 
			break;
		if(strcmp(tmpchar1, ">") == 0 && tmpchar2[0] == '<')
			strcpy(feature[fnum++], tmpchar2);
	}	
	
if(ifield == 1) {
	for(i=0;i<fnum-1;i++) {
		for(j=1;j<strlen(feature[i])-1; j++)
			fprintf(fpout, "%c", feature[i][j]);	
		if(delimiter == 0)
			fprintf(fpout, "\t");	
		else
			fprintf(fpout, " , ");	
	}
	for(j=1;j<strlen(feature[fnum-1])-1; j++)
		fprintf(fpout, "%c", feature[fnum-1][j]);	
	fprintf(fpout, "\n");	
}
for(i=0;i<fnum;i++)
	strcpy(value[i], "-99999");
rewind(fpin); 
for(;;) {
	if(fgets(line,MAXCHAR,fpin) ==NULL) break;
	strcpy(tmpchar1, "");
	strcpy(tmpchar2, "");
       	sscanf(line, "%s%s", tmpchar1, tmpchar2);
	if(strncmp(tmpchar1, "$$$$", 4) == 0){
		for(i=0;i<fnum-1;i++) {
			fprintf(fpout, "%s", value[i]);	
			if(delimiter == 0)
				fprintf(fpout, "\t");	
			else
				fprintf(fpout, " , ");	
			strcpy(value[i], "-99999");
		}
		fprintf(fpout, "%s\n", value[fnum-1]);	
		strcpy(value[fnum-1], "-99999");
	}	
	if(strcmp(tmpchar1, ">") == 0 && tmpchar2[0] == '<')
		for(i=0;i<fnum;i++) 
			if(strcmp(feature[i], tmpchar2)==0){
				strcpy(line, "");
				line[0]= '\0';
				fgets(line,MAXCHAR,fpin);
				strcpy(tmpchar3, "");
				if(ftype[i] == 0) {
       					sscanf(line, "%s", tmpchar3);
					strcpy(value[i], tmpchar3);
				}
				else {
					strcpy(value[i], line);
					value[i][strlen(line)-1] = '\0';
				}
				break;
			}
}	
fclose(fpin);
fclose(fpout);
} 
