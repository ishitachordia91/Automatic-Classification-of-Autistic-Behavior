%% Load files
%% choose data folder
% dataFolder=uigetdir('E:\20120706_MatthewGoodwin&JasonNawyn_Study2Wockets\001','Select Data Folder fot Analysing');

%% load raw data and store in a cell
    % Wocket_00_RawCorrectedData_RightWrist=csvread([dataFolder,'Wocket_00_RawCorrectedData_Right-Wrist.csv']);
    Wocket_00_RawCorrectedData_RightWrist=csvread('Wocket_00_RawCorrectedData_Right-Wrist.csv');
    Wocket_01_RawCorrectedData_LeftWrist=csvread('Wocket_01_RawCorrectedData_Left-Wrist.csv');
    Wocket_02_RawCorrectedData_Torso=csvread('Wocket_02_RawCorrectedData_Torso.csv');
%     Wocket_00_RawCorrectedData_RightWrist=csvread('Wocket_00_RawCorrectedData_Right-Wrist.csv');
%     Wocket_01_RawCorrectedData_LeftWrist=csvread('Wocket_01_RawCorrectedData_Left-Wrist.csv');
%     Wocket_02_RawCorrectedData_Torso=csvread('Wocket_02_RawCorrectedData_Torso.csv');
    rawData={Wocket_00_RawCorrectedData_RightWrist,Wocket_01_RawCorrectedData_LeftWrist,Wocket_02_RawCorrectedData_Torso};
    clear Wocket_00_RawCorrectedData_RightWrist;
    clear Wocket_01_RawCorrectedData_LeftWrist;
    clear Wocket_02_RawCorrectedData_Torso;
    
    % load phone and video annotation excel sheets and store in a cell
     %phoneAnnotationIntervals=csv2cell('AnnotationIntervals.csv');
   

    
    
    %     video annotator1

    [eeA,videoAnnotation1t,eeC1]=xlsread('AnnotationVideo1Intervals.xlsx',1,'A:F');
    videoAnnotationIntervals1t=[videoAnnotation1t(2:end,3) videoAnnotation1t(2:end,1) videoAnnotation1t(2:end,6) videoAnnotation1t(2:end,6)];
    [eeA,videoAnnotation1goodData,eeC1]=xlsread('Annotator1Stereotypy.annotation.xlsx',1,'K:L');
    videoAnnotation1goodDataStart=char(videoAnnotation1goodData(2,1));
    videoAnnotation1goodDataEnd=char(videoAnnotation1goodData(2,2));
    goodDataRow1=[cellstr(videoAnnotation1goodDataEnd(end-11:end)) 0 cellstr(videoAnnotation1goodDataStart(end-11:end))];
    videoAnnotation1=[videoAnnotation1t(2,2:4);goodDataRow1;goodDataRow1;videoAnnotation1t(3:end,2:4)];
    goodDataRow2=[cellstr(videoAnnotation1goodDataStart(1:end-4)) cellstr(videoAnnotation1goodDataEnd(1:end-4)) 0 cellstr('sync')];
    videoAnnotationIntervals1=[videoAnnotationIntervals1t(1,:);goodDataRow2;goodDataRow2;videoAnnotationIntervals1t(2:end,:)];
    
    %     video annotator2
    [eeA,videoAnnotation2t,eeC1]=xlsread('AnnotationVideo2Intervals.xlsx',1,'A:F');
    videoAnnotationIntervals2t=[videoAnnotation2t(2:end,3) videoAnnotation2t(2:end,1) videoAnnotation2t(2:end,6) videoAnnotation2t(2:end,6)];
    [eeA,videoAnnotation2goodData,eeC1]=xlsread('Annotator2Stereotypy.annotation.xlsx',1,'K:L');
    videoAnnotation2goodDataStart=char(videoAnnotation2goodData(2,1));
    videoAnnotation2goodDataEnd=char(videoAnnotation2goodData(2,2));
    goodDataRow3=[cellstr(videoAnnotation2goodDataEnd(end-11:end)) 0 cellstr(videoAnnotation2goodDataStart(end-11:end))];
    videoAnnotation2=[videoAnnotation2t(2,2:4);goodDataRow3;goodDataRow3;videoAnnotation2t(3:end,2:4)];
    goodDataRow4=[cellstr(videoAnnotation2goodDataStart(1:end-4)) cellstr(videoAnnotation2goodDataEnd(1:end-4)) 0 cellstr('sync')];
    videoAnnotationIntervals2=[videoAnnotationIntervals2t(1,:);goodDataRow4;goodDataRow4;videoAnnotationIntervals2t(2:end,:)];
    

    % videoAnnotation=[videoAnnotation;{''}];
    %phoneAnnotationIntervals=phoneAnnotationIntervals(1:end,:);
    videoAnnotationIntervals1=videoAnnotationIntervals1(1:end,:);
    videoAnnotationIntervals2=videoAnnotationIntervals2(1:end,:);
    % rawAnnotation={phoneAnnotation,videoAnnotation,videoAnnotationTime,AnnotationIntervals};
    rawAnnotation={videoAnnotation1,videoAnnotationIntervals1,videoAnnotation1,videoAnnotationIntervals1,videoAnnotation2,videoAnnotationIntervals2};
    clear eeA;clear eeC1;clear videoAnnotation1;
    clear videoAnnotation2;
    clear videoAnnotationIntervals1t;clear videoAnnotationIntervals2t;
    clear videoAnnotation1t;clear videoAnnotation2t;
    clear videoAnnotationTime0;clear videoAnnotationTime;
    clear videoAnnotation2goodData;clear videoAnnotation1goodData;
% load Filter
load('Hd.mat');
