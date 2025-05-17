function DataPortBytesAvailableHandler( obj, event, handles )
% obj:      serial port object
% event:    event information
% handles:  handles

i_foldername = get(handles.edit19, 'String');
path = ['experiment', i_foldername];
settingfilename = fullfile(path,'setting_information.txt');
timefilename = fullfile(path,'time.dat');

if ~exist(settingfilename,'file')
    display('Information record incomplete');
    msgbox('Information record incomplete','warning','error')
else

    if (get(handles.AutoScale, 'Value') == get(handles.AutoScale, 'Max'))
        display('Auto-Scaling on');
    else
        display('Auto-Scaling off');
    end
    %Autoscale = 0;
    Autoscale = get(handles.AutoScale, 'Value');

    %code added by Tao
 %   VideoRecord = get(handles.radiobutton11, 'Value'); %if record picture for video generation during record procedure
    tensmode = get(handles.radiobutton12, 'Value'); %if trace mode is set to 10s


    minADC = get(handles.edit26, 'String');
    maxADC= get(handles.edit27, 'String');
   

    %minADC=str2double (minADC);
    %maxADC=str2double (maxADC);
    
     

 %code added by Tao ended

    RefPackets = [3,8]; %enter negative number if no reference frame (under construction)
    
    tNow = now; %record event time
    
    %Temporary try construction for debug purposes only:
    try
        handles = guidata(handles.start_data_read); %obtain most recent version of handles
        if handles.datacom_s.UserData.CaptureData








            %Read packet from serial port for data:
            packetNumberBytes = fread(obj,4,'uint8'); %column vector (4 elements)

            %check by Tao
            %packetDataBytes = fread(obj,12*1024,'uint8'); %matrix (12 rows, 1024 columns)
            packetDataBytes = fread(obj,[12,1024],'uint8'); %matrix (12 rows, 1024 columns)
            %Write packet to output file for data (same format as with previous datagrabber.exe):
            fwrite(handles.dataout,packetNumberBytes,'uint8');
            fwrite(handles.dataout,packetDataBytes,'uint8');
            packetNumber = [1677216,65536,256,1] * packetNumberBytes;
            %Decoding packet data:
            
            %packetDataMasks = [1,2,4,8,16,32]; %masks for decoding the ADC bits the 6 channels from the bytes of packetDataBytes

%code added by Tao for new PIN/DMA channel using
            packetDataMasks = [16,32,64]; %MASKS, BIT6(p0.5) for RA/B, BIT 5(p0.4) for RD/E, BIT 7(p0.6) for RG/H, change the order later in channel();


            %Samples = zeros(6,1024); %preallocate memory for Samples (check if this can be speeded up if Samples is retained over subsequent calls)
            Samples = zeros(3,1024); %preallocate memory for Samples (check if this can be speeded up if Samples is retained over subsequent calls)
          
    
            %for n = 1:6
            for n = 1:3
            %    Samples(n,:) = [2048,1024,512,256,128,64,32,16,8,4,2,1] * bitshift(bitand(packetDataBytes,packetDataMasks(n)),1-n); %decode smaples from packet data bytes
              Samples(n,:) = [2048,1024,512,256,128,64,32,16,8,4,2,1] * bitshift(bitand(packetDataBytes,packetDataMasks(n)),-3-n); %decode smaples from packet data bytes
          %using bit 5-7, bitshift to right 4-6
                 Samples(n,1024) = 0; %invalid sample in case of Single Cell scan mode --> Make consistent with user-selected scan mode
          
       
            end
    
     %added by Tao
    %   global datavoltage
    %   global packnumber
    %   packnumber=packetNumber;
    %   datavoltage=Samples;
    
        %guidata(handles.packnumber,packetNumber);
        %guidata(handles.datavoltage,Samples);
        handles.packnumber=packetNumber;
        handles.datavoltage=Samples;
    
    
    %eval([writematrix,'(Samples',',','myData_',num2str(packetNumber),'.dat',',','Delimiter',',',';)']);
    % writematrix([packetNumber,1],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
    % writematrix(Samples(1,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
    % writematrix([packetNumber,3],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
    % writematrix(Samples(3,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append') 
    % writematrix([packetNumber,5],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')
    % writematrix(Samples(5,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
    % writematrix(packetNumber+1,'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
    %type myData.dat
      %end of code added by Tao      
    
    
            
    %        Channels = [1, 3, 5]; %temporary fixed selection of channels A, D and G -> to be made consistent with user-selected channels and scan mode
           % Channels = [2, 4, 6]; %temporary fixed selection of channels B, E and H -> to be made consistent with user-selected channels and scan mode
            
    % code added by Tao
            Channels = [2, 1, 3];%now only 3 channels' data will be transferred to pc
                      
           
           for nA = 1:3 %temporal fixed number of sensing fields -> should be made consistent with variable number of sensing fields in initialization functions
                nCh = Channels(nA);
                K = handles.SensingFields.K(nA);
                L = handles.SensingFields.L(nA);
                nR = handles.SensingFields.Resolution(nA);
                M = handles.SensingFields.M(nA,nR);
                N = handles.SensingFields.N(nA,nR);
                M1 = handles.SensingFields.M1(nA,nR);
                N1 = handles.SensingFields.N1(nA,nR);
                N2 = N-N1;
                
                %Construct reference samples and subtract:
                if packetNumber >= RefPackets(1) && packetNumber <= RefPackets(2)
                    handles.SamplesReference(nA,:) = handles.SamplesReference(nA,:)+Samples(nCh,:)/(RefPackets(2)-RefPackets(1)+1); %accumulate reference packets
                end
                Samples(nCh,:) = Samples(nCh,:)-handles.SamplesReference(nA,:);
                
                V = zeros(M1+(K+1)*M,(L+1)*N-N1); %prealocation and/or initialization
                KernelMatrixOdd = handles.Interpolation.KernelMatricesOdd{nA};
                KernelMatrixEven = handles.Interpolation.KernelMatricesEven{nA};
                for i = 1:K
                    for j = 1:L
                        V(1+(i-1)*M:2*M+(i-1)*M,1+(j-1)*N:N+(j-1)*N) = V(1+(i-1)*M:2*M+(i-1)*M,1+(j-1)*N:N+(j-1)*N) + KernelMatrixOdd * Samples(nCh,i+(j-1)*2*K);
                        V(M1+1+(i-1)*M:M1+2*M+(i-1)*M,N2+1+(j-1)*N:N2+N+(j-1)*N) = V(M1+1+(i-1)*M:M1+2*M+(i-1)*M,N2+1+(j-1)*N:N2+N+(j-1)*N) + KernelMatrixEven * Samples(nCh,1+j*2*K-i);
                    end
                end
                
    %Scaling of bitmaps based on confidence boundaries:
                if Autoscale ~= 0
                    %Bitmap plots:
                    CF = handles.ConfidenceFactor(nA);
                    V_Center = mean(Samples(nCh,1:1023));
                    %V_Center = mean([Samples(nCh,1:676),Samples(nCh,678:1023)]); %exclude the ESD-damaged pixel of sensor 04
                    V_Std = std(Samples(nCh,1:1023));
                    %V_Std = std([Samples(nCh,1:676),Samples(nCh,678:1023)]); %exclude the ESD-damaged pixel of sensor 04
                    if V_Std ~= 0
                        set(handles.SubPlots(nA),'CLim', [V_Center-CF*V_Std, V_Center+CF*V_Std]);
                    end    

                end
                set(handles.Images(nA),'CData',V); %fast update of bitmap image
%code added by Tao
                if isempty(minADC) ==0 && isempty (maxADC) ==0
                        set(handles.SubPlots(nA),'CLim', [str2double(minADC), str2double(maxADC)]);
                end
%code added by Tao ended




                %Cumulative distribution function (CDF) plots:
                X = sort(Samples(nCh,1:1023));
                set(handles.CDF_Plot(nA),'XData',X,'YData',0.5/1023 : 1/1023 : (1023-0.5)/1023); %fast update of CDF plot
                %axes(handles.SubPlots(3+nA)); %make figure current
    %Scaling of CDFs to fixed limits:
                %Xlims = [1200,1400;1750,1950;1630,1830]; %sensor 21 at 40 MHz
                %Xlims = [1850,2050;1750,2050;1730,1930]; %sensor 04 at 40 MHz
                %set(handles.SubPlots(3+nA),'XLim',Xlims(nA,:));
    %Scaling of CDFs based on confidence boundaries:
                
                if Autoscale ~= 0 && V_Std ~= 0 
                    set(handles.SubPlots(3+nA),'XLim',[V_Center-CF*V_Std,V_Center+CF*V_Std]); %scaling to confidence bounderies
                end
%code added by Tao
                if isempty(minADC) ==0 && isempty (maxADC) ==0
                    set(handles.SubPlots(3+nA),'XLim',[str2double(minADC),str2double(maxADC)]);
                end
%code added by Tao ended

                %Default  autoscaling of CDFs:
                %set(handles.SubPlots(3+nA),'XLimMode','auto'); %autoscaling
                


                %Signal trace plots:

    

     %code added by Tao
        st1m1=str2num(get(handles.edit1m1,'string'));
        st1m2=str2num(get(handles.edit1m2,'string'));
        st1m3=str2num(get(handles.edit1m3,'string'));
        st1m4=str2num(get(handles.edit1m4,'string'));
        st1m5=str2num(get(handles.edit1m5,'string'));
        st2m1=str2num(get(handles.edit2m1,'string'));
        st2m2=str2num(get(handles.edit2m2,'string'));
        st2m3=str2num(get(handles.edit2m3,'string'));
        st2m4=str2num(get(handles.edit2m4,'string'));
        st2m5=str2num(get(handles.edit2m5,'string'));
        st3m1=str2num(get(handles.edit3m1,'string'));
        st3m2=str2num(get(handles.edit3m2,'string'));
        st3m3=str2num(get(handles.edit3m3,'string'));
        st3m4=str2num(get(handles.edit3m4,'string'));
        st3m5=str2num(get(handles.edit3m5,'string'));

       % guidata(handles.output, handles);

        if Autoscale ~= 0 && V_Std ~= 0 
                    set(handles.SubPlots(6+nA),'YLim',[V_Center-CF*V_Std,V_Center+CF*V_Std]); %scaling to confidence bounderies
        end
                
       if isempty(minADC) ==0 && isempty (maxADC) ==0
                     set(handles.SubPlots(6+nA),'YLim',[str2double(minADC),str2double(maxADC)]);
       end         




       

       




       if nA==1 

                %code added by Tao
                x1=handles.x1;  %calculate X once for 3 parallel channels, for signal trace
                tnow = datevec(tNow);
                tlast = datevec(handles.tLast);
                    judgement=tnow(1,5)-tlast(1,5);
                    if judgement ==0
                        x1=x1+tnow(1,6)-tlast(1,6); 
                    else 
                        x1=x1+60+tnow(1,6)-tlast(1,6);
                    end
                handles.x1=x1;
                
                X1=handles.X1;
                tensjudge=size(X1);
                if tensjudge(1,2)>=50  && tensmode~=0
                    X1=X1(end-49:end);
                    X1=[X1,x1];
                    X1=X1-x1+10;
                    handles.x1=10;
                else 
                    X1=[X1,x1];
                end
                handles.X1=X1;
                %code added by Tao ended



%             x=handles.x;
%             X=handles.X;
                if isempty(st1m1)==0
                    y11=Samples(2,st1m1);

                    Y11=handles.Y11;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y11=Y11(end-49:end);
                    end
                        Y11=[Y11,y11];
                    
                    handles.Y11=Y11;
                  
                   
                    set(handles.SignalTracePlot1(nA),'XData',X1,'YData',Y11); %fast update of sinal trace plots
                end
                if isempty(st1m2)==0
                    y12=Samples(2,st1m2);
                    Y12=handles.Y12;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y12=Y12(end-49:end);
                    end
                        Y12=[Y12,y12];

                    handles.Y12=Y12;
                    set(handles.SignalTracePlot2(nA),'XData',X1,'YData',Y12); %fast update of sinal trace plots
                end
                if isempty(st1m3)==0
                    y13=Samples(2,st1m3);
                    Y13=handles.Y13;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y13=Y13(end-49:end);
                    end
                    Y13=[Y13,y13];
                    handles.Y13=Y13;
                    set(handles.SignalTracePlot3(nA),'XData',X1,'YData',Y13); %fast update of sinal trace plots
                end
                if isempty(st1m4)==0
                    y14=Samples(2,st1m4);
                    Y14=handles.Y14;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y14=Y14(end-49:end);
                    end
                    Y14=[Y14,y14];
                    handles.Y14=Y14;
                    set(handles.SignalTracePlot4(nA),'XData',X1,'YData',Y14); %fast update of sinal trace plots
                end
                if isempty(st1m5)==0
                    y15=Samples(2,st1m5);
                    Y15=handles.Y15;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y15=Y15(end-49:end);
                    end
                    Y15=[Y15,y15];
                    handles.Y15=Y15;
                    set(handles.SignalTracePlot5(nA),'XData',X1,'YData',Y15); %fast update of sinal trace plots
                end

                if tensmode~=0
                    set(handles.SubPlots(6+nA),'XLim',[0,10]);
                elseif isempty(get(handles.edit47,'string'))==1 
                    set(handles.SubPlots(6+nA),'XLim',[0,5*x1]);
                else
                    tracelimit=str2double(get(handles.edit47,'string'));
                    set(handles.SubPlots(6+nA),'XLim',[0,tracelimit]);
                end
       end
       if nA==2     

                x2=handles.x2;  %calculate X once for 3 parallel channels, for signal trace
                tnow = datevec(tNow);
                tlast = datevec(handles.tLast);
                    judgement=tnow(1,5)-tlast(1,5);
                    if judgement ==0
                        x2=x2+tnow(1,6)-tlast(1,6); 
                    else 
                        x2=x2+60+tnow(1,6)-tlast(1,6);
                    end                
                    handles.x2=x2;
                
                X2=handles.X2;
                tensjudge=size(X2);
                if tensjudge(1,2)>=50  && tensmode~=0
                    X2=X2(end-49:end);
                    X2=[X2,x2];
                    X2=X2-x2+10;
                    handles.x2=10;
                else 
                    X2=[X2,x2];
                end
                handles.X2=X2;
%            x=handles.x;
%            X=handles.X;
                if isempty(st2m1)==0
                    y21=Samples(1,st2m1);
                    Y21=handles.Y21;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y21=Y21(end-49:end);
                    end
                    Y21=[Y21,y21];
                    handles.Y21=Y21;


                    set(handles.SignalTracePlot1(nA),'XData',X2,'YData',Y21); %fast update of sinal trace plots
                end
                if isempty(st2m2)==0
                    y22=Samples(1,st2m2);
                    Y22=handles.Y22;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y22=Y22(end-49:end);
                    end
                    Y22=[Y22,y22];
                    handles.Y22=Y22;

                    set(handles.SignalTracePlot2(nA),'XData',X2,'YData',Y22); %fast update of sinal trace plots
                end
                if isempty(st2m3)==0
                    y23=Samples(1,st2m3);
                    Y23=handles.Y23;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y23=Y23(end-49:end);
                    end
                    Y23=[Y23,y23];
                    handles.Y23=Y23;
                    set(handles.SignalTracePlot3(nA),'XData',X2,'YData',Y23); %fast update of sinal trace plots
                end
                if isempty(st2m4)==0
                    y24=Samples(1,st2m4);
                    Y24=handles.Y24;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y24=Y24(end-49:end);
                    end
                    Y24=[Y24,y24];
                    handles.Y24=Y24;
                    set(handles.SignalTracePlot4(nA),'XData',X2,'YData',Y24); %fast update of sinal trace plots
                end
                if isempty(st2m5)==0
                    y25=Samples(1,st2m5);
                    Y25=handles.Y25;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y25=Y25(end-49:end);
                    end
                    Y25=[Y25,y25];
                    handles.Y25=Y25;
                    set(handles.SignalTracePlot5(nA),'XData',X2,'YData',Y25); %fast update of sinal trace plots
                end
               if tensmode~=0
                    set(handles.SubPlots(6+nA),'XLim',[0,10]);
                elseif isempty(get(handles.edit47,'string'))==1 
                    set(handles.SubPlots(6+nA),'XLim',[0,5*x1]);
                else
                    tracelimit=str2double(get(handles.edit47,'string'));
                    set(handles.SubPlots(6+nA),'XLim',[0,tracelimit]);
                end
        end

        if nA==3      

                x3=handles.x3;  %calculate X once for 3 parallel channels, for signal trace
                tnow = datevec(tNow);
                tlast = datevec(handles.tLast);
                    judgement=tnow(1,5)-tlast(1,5);
                    if judgement ==0
                        x3=x3+tnow(1,6)-tlast(1,6); 
                    else 
                        x3=x3+60+tnow(1,6)-tlast(1,6);
                    end
                handles.x3=x3;

                X3=handles.X3;
                tensjudge=size(X3);
                if tensjudge(1,2)>=50  && tensmode~=0
                    X3=X3(end-49:end);
                    X3=[X3,x3];
                    X3=X3-x3+10;
                    handles.x3=10;
                else 
                    X3=[X3,x3];
                end
                handles.X3=X3;
%             x=handles.x;
%             X=handles.X;
                if isempty(st3m1)==0
                    y31=Samples(3,st3m1);
                    Y31=handles.Y31;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y31=Y31(end-49:end);
                    end
                    Y31=[Y31,y31];
                    handles.Y31=Y31;
                    set(handles.SignalTracePlot1(nA),'XData',X3,'YData',Y31); %fast update of sinal trace plots
                end
                if isempty(st3m2)==0
                    y32=Samples(3,st3m2);
                    Y32=handles.Y32;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y32=Y32(end-49:end);
                    end
                    Y32=[Y32,y32];
                    handles.Y32=Y32;
                    set(handles.SignalTracePlot2(nA),'XData',X3,'YData',Y32); %fast update of sinal trace plots
                end
                if isempty(st3m3)==0
                    y33=Samples(3,st3m3);
                    Y33=handles.Y33;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y33=Y33(end-49:end);
                    end
                    Y33=[Y33,y33];
                    handles.Y33=Y33;
                    set(handles.SignalTracePlot3(nA),'XData',X3,'YData',Y33); %fast update of sinal trace plots
                end
                if isempty(st3m4)==0
                    y34=Samples(3,st3m4);
                    Y34=handles.Y34;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y34=Y34(end-49:end);
                    end
                    Y34=[Y34,y34];
                    handles.Y34=Y34;
                    set(handles.SignalTracePlot4(nA),'XData',X3,'YData',Y34); %fast update of sinal trace plots
                end
                if isempty(st3m5)==0
                    y35=Samples(3,st3m5);
                    Y35=handles.Y35;
                    if tensjudge(1,2)>=50  && tensmode~=0
                        Y35=Y35(end-49:end);
                    end
                    Y35=[Y35,y35];
                    handles.Y35=Y35;
                    set(handles.SignalTracePlot5(nA),'XData',X3,'YData',Y35); %fast update of sinal trace plots
                end
                if tensmode~=0
                    set(handles.SubPlots(6+nA),'XLim',[0,10]);
                elseif isempty(get(handles.edit47,'string'))==1 
                    set(handles.SubPlots(6+nA),'XLim',[0,5*x1]);
                else
                    tracelimit=str2double(get(handles.edit47,'string'));
                    set(handles.SubPlots(6+nA),'XLim',[0,tracelimit]);
                end
        end
        
        

        
     %code added by Tao ended




    
            end
    
            tr=fopen(timefilename,'a+');
            fprintf(tr,'%9f\r\n',now);
            fclose(tr);
    
    
            
            %Debugging output to Command Window:
            dt = tNow-handles.tLast;
            handles.tLast = tNow; %remember time of last call
            display(sprintf('packet number %d at date and time: %s; time interval: %s',packetNumber,datestr(event.Data.AbsTime,'dd-mmm-yyyy HH:MM:SS.FFF'),datestr(dt,'SS.FFF')));
            
            
    
    
    
    
                %code added by Tao
           
            
               if (get(handles.togglebutton18, 'Value') == get(handles.togglebutton18, 'Max'))
              %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %                     global datavoltage
    %                     global packnumber
               
    
                display(sprintf('still recording'));
            
    
               % pause(1);
    
    %            datavoltage=handles.datavoltage;
                packnumber=handles.packnumber;
    
                %datavoltage=Samples;
                %eval([writematrix,'(Samples',',','myData_',num2str(packetNumber),'.dat',',','Delimiter',',',';)']);
                
                %eval([writematrix,'(Samples',',','myData_',num2str(packetNumber),'.dat',',','Delimiter',',',';)']);
%                     writematrix([packnumber,1],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
%                     writematrix(datavoltage(1,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
%                     writematrix([packnumber,3],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
%                     writematrix(datavoltage(3,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append') 
%                     writematrix([packnumber,5],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')
%                     writematrix(datavoltage(5,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  


 %               myData_record = fullfile(path,'myData.dat');
                
                


                 %writematrix(tNow,maData_record,'Delimiter','tab', 'WriteMode' , 'append')  
 %                writematrix(datestr(event.Data.AbsTime,'dd-mmm-yyyy HH:MM:SS.FFF'),myData_record,'Delimiter','tab', 'WriteMode' , 'append')  
                 %writematrix(datestr(tNow,'dd-mmm-yyyy HH:MM:SS'),myData_record,'Delimiter','tab', 'WriteMode' , 'append') 
 %                writematrix([packnumber,1],myData_record,'Delimiter','tab', 'WriteMode' , 'append')  
 %                writematrix(datavoltage(2,:),myData_record,'Delimiter','tab', 'WriteMode' , 'append')  
 %                writematrix([2],myData_record,'Delimiter','tab', 'WriteMode' , 'append')  
 %                writematrix(datavoltage(1,:),myData_record,'Delimiter','tab', 'WriteMode' , 'append') 
 %                writematrix([3],myData_record,'Delimiter','tab', 'WriteMode' , 'append')
 %                writematrix(datavoltage(3,:),myData_record,'Delimiter','tab', 'WriteMode' , 'append')  


    %            if VideoRecord~=0
                    saveas(handles.SensorData, [path,'/output',num2str(packnumber)], 'png')
                    record = fullfile(path,'record.txt');   %packet number record file, for check purpose in video generation function       
                    writematrix([packnumber],record,'Delimiter','tab', 'WriteMode' , 'append');

    %            end

            
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                



                 %writematrix(packetNumber+1,'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
    
                     % type myData.dat
    
                     %save picture with gui interface
    
                    %saveas(gcf, ['output',num2str(packnumber)], 'bmp')


                
                    
              


               else
                               
                    display(sprintf('not recording'));
               
               end
    
    




                %added by Tao for new code without RTK
            fwrite(obj,7,'uint8');

%            cmd = 'cap 777';
%            fprintf(handles.s, cmd);
    









    
    
            %code added by Tao
    %         buttonstate=handles.record_state;
    %         display(sprintf('buttonstate %d',buttonstate));
    %         global reco
    %         display(sprintf('reco %d',reco));
    
            %code added by Tao ended
    
    
            
            guidata(handles.start_data_read,handles); %store new local handles into object
        end
    catch err_DataPortBytesAvailableHandler
        display(err_DataPortBytesAvailableHandler);
    end
    
    end
end
