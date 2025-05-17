function DataPortErrorHandler( obj, event, handles )
% obj:      serial port object
% event:    event information
% handles:  handles

%Temporary try construction for debug purposes only:
try
    handles = guidata(handles.start_data_read); %use most recent version of handles
    %Preliminary error handling:
    display('DataPortErrorHandler: error hanling to be completed yet');

catch err_DataPortErrorHandler
    display(err_DataPortErrorHandler);
end

end

