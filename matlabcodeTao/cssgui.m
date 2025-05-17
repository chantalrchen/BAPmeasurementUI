function varargout = cssgui(varargin)
% CSSGUI MATLAB code for cssgui.fig
%      CSSGUI, by itself, creates a new CSSGUI or raises the existing
%      singleton*.
%
%      H = CSSGUI returns the handle to a new CSSGUI or the handle to
%      the existing singleton*.
%
%      CSSGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CSSGUI.M with the given input arguments.
%
%      CSSGUI('Property','Value',...) creates a new CSSGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before cssgui_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to cssgui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% Make executable: http://www.mathworks.nl/products/compiler/description1.html
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help cssgui

% Last Modified by GUIDE v2.5 23-Sep-2024 14:40:37

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @cssgui_OpeningFcn, ...
                   'gui_OutputFcn',  @cssgui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT
global clk_availfreq;
clk_availfreq = {'off' '25' '30' '35' '40' '45' '50' '55' '60' '65' '70' '75' '80' '85' '90' '100'};
global dac_availdac;
dac_availdac = {'Vddd' 'Vdda' 'Vcfi' 'Vbias'};
global debug_values;
debug_values = {'NONE', 0; 'RSP', 1; 'FATAL', 2; 'ERR  ', 3; 'WARN ', 4; 'INFO ', 5; 'DBG  ', 6};

%------------------
% utility functions
%------------------
function visibility_all(handles, value)
    set(handles.com_panel, 'Visible', value);
    set(handles.clk_panel, 'Visible', value);
    set(handles.dac_panel, 'Visible', value);
    set(handles.dac_maxpanel, 'Visible', value);
    set(handles.cmdfile_panel, 'Visible', value);
    set(handles.debug_panel, 'Visible', value);

    %code added by Tao
    set(handles.notes_panel, 'Visible', value);
    set(handles.settings_panel, 'Visible', value);
    %code added by Tao ended

    set(handles.datamanual_panel, 'Visible', value);
    set(handles.datadma_panel, 'Visible', value);

 

%----------------------
% end utility functions
%----------------------

% --- Executes just before cssgui is made visible.
function cssgui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to cssgui (see VARARGIN)

% Choose default command line output for cssgui
handles.output = hObject;

% make all panels invisible. Make them visible again after init of the
% specific panel is done.
visibility_all(handles, 'off');

% All panels are created in one GUI using GUIDE. Then use this code to
% split the panels over several tabs. The tabs need to be repositioned at
% every tab. Finally the size of the GUI can be reduced.
% When running this app, you get a warning: The uitabgroup object is
% undocumented and some of its properties will become obsolete in a future
% release. As long as we use R2012b, this should not  be a problem.
tabgroup = uitabgroup(hObject);
tab1 = uitab(tabgroup, 'Title', 'Basic Settings');
tab2 = uitab(tabgroup, 'Title', 'Advanced Settings');
tab3 = uitab(tabgroup, 'Title', 'Data');
uistack(handles.msg_panel, 'top');
set(handles.basicsettings_panel,    'Parent', tab1, 'Position', [2 7.6 99 37]);
set(handles.advancedsettings_panel, 'Parent', tab2, 'Position', [2 7.6 99 37]);
set(handles.data_panel,             'Parent', tab3, 'Position', [2 7.6 99 37]);
set(hObject, 'Position', [0 0 102 47]);

% Update handles structure
guidata(hObject, handles);
% closes all open serial ports in case they were not closed properly before
newobjs = instrfind;
delete(newobjs);


% UIWAIT makes cssgui wait for user response (see UIRESUME)
% uiwait(handles.figure1);

% --- Outputs from this function are returned to the command line.
function varargout = cssgui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

%% --------------------------------
% COM PORT
% ---------------------------------
% This comport is used for sending commands and receiving messages.
% com_val:      a text input that allows the user to set the com port for
%               sending commands and receiving messages
% cmd_com_open: a togglebutton to open/close the command comport
% ---------------------------------

% --- Executes on  change in com_val.
function com_val_Callback(hObject, eventdata, handles)
% hObject    handle to com_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of com_val as text
%        str2double(get(hObject,'String')) returns contents of com_val as a double

% --- Executes during object creation, after setting all properties.
function com_val_CreateFcn(hObject, eventdata, handles)
% hObject    handle to com_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

% --- Executes on button press in cmd_com_open.
function cmd_com_open_Callback(hObject, eventdata, handles)
    % hObject    handle to cmd_com_open (see GCBO)
    % eventdata  reserved - to be defined in a future version of MATLAB
    % handles    structure with handles and user data (see GUIDATA)

    button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    % At startup, button_state is set to 'Min'.
    if (button_state == min) 
        try
            if (~handles.com_opened) % Only open once
                handles.com_port = get(handles.com_val, 'String'); % store the opened comport, simply to close the same port later on
                handles.s = serial(handles.com_port);
                set(handles.s, 'baudrate', 115200);

                % Setup a callback that is called everytime a terminator is received
                set(handles.s, 'BytesAvailableFcnMode', 'terminator');

                set(handles.s, 'BytesAvailableFcn', {@com_eventhandler, handles}); %argument list modified by Frans
                 
                fopen(handles.s);
                handles.com_opened = true;
                set(hObject, 'String', 'Close'); 
                set(handles.msg_display, 'String', sprintf('Opened comport %s\n', handles.com_port));

                guidata(hObject, handles); % Update handles structure
                
            end
        catch ME
            set(handles.msg_display, 'String', ME.message);
            set(hObject, 'Value', max); % Open failed. GUI should stay in 'Closed' mode. However, a toggle has occurred. Manually toggle again.
        end
    elseif (button_state == max)
        try
            if (handles.com_opened) % only close when port is opened
                fclose(handles.s);
                handles.com_opened = false;
                set(handles.cmd_com_open, 'String', 'Open');
                set(handles.msg_display, 'String', sprintf('Closed comport %s\n', handles.com_port));
            else
                set(handles.msg_display, 'String', 'Cannot close. Comport not opened');
            end
            guidata(hObject, handles); % Update handles structure
        catch ME
            set(handles.msg_display, 'String', ME.message);
            set(hObject, 'Value', min); % Close failed. GUI should stay in 'Closed' mode. However, a toggle has occurred. Manually toggle again.
        end

    end

% http://www.mathworks.nl/matlabcentral/fileexchange/26371-simple-gui-for-serial-port-communication
% http://www.mathworks.com/matlabcentral/fileexchange/31958-serialdatastream/content/serialDataStream.m
% This callback is called whenever a terminator charater arrives at the com port.
% The data arriving can be one of the following:
% - a response to a command                           -> store all responses in output file, only show response to readall in message window
% - info from the LPC                                 -> store all info in output file, show in message window
% - an error message from the LPC                     -> store all errors in output file, show in message window
% - an echo from the command that was sent to the LPC -> ignore

%function com_eventhandler(obj, event, msg_display, read_result, outfileID)
%function header modified by Frans:
function com_eventhandler(obj, event, handles)  %pass full handles structure instead of seperate handles fields (Frans)
    msg_display = handles.msg_display;          %local variable instead of function argument (Frans)
    read_result = handles.read_result;          %local variable instead of function argument (Frans)
    outfileID = handles.outfileID;              %local variable instead of function argument (Frans)
    
    now = java.lang.System.currentTimeMillis; %http://practicalmatlab.com/
    
    if strcmp(event.Type, 'BytesAvailable')
        bytes = get(obj, 'BytesAvailable');
        if (bytes > 0)
            msg = fscanf(obj);
            % prepare message to write to file
            msg2 = sprintf('%d %s\n', now, msg);

            % response to a command
            if (strfind(msg, 'caprsp') == 1)
                if (strfind(msg, 'caprsp readall') == 1)
                    set(read_result, 'String', msg);
                else
                    %display(msg);
                end
                fprintf(outfileID, '%s\n', msg2);
            % message from LPC
            elseif (strfind(msg, 'capmsg') == 1)
                set(msg_display, 'String', msg);
                fprintf(outfileID, '%s\n', msg2);
            % Error message from LPC
            elseif (strfind(msg, 'caperr') > 0)
                set(msg_display, 'String', msg);
                fprintf(outfileID, '%s\n', msg2);
            % echo from command sent over serial port
            elseif (strfind(msg, 'cap ') > 0)
            else
                fprintf(outfileID, '%s\n', msg2);
            end
        end
    end

% Send a command over the com port to the LPC. Log the command and a
% timestamp in the logfile.
function com_sendcmd(handles, cmd)
    try
        if (handles.com_opened)
            if (~isempty(cmd))
                fprintf(handles.s, cmd);
                now = java.lang.System.currentTimeMillis; %http://practicalmatlab.com/
                logcmd = sprintf('%d %s\n', now, cmd);
                fprintf(handles.logfileID, '%s\r\n', logcmd);
                set(handles.msg_display, 'String', cmd);
            else
%                display('Empty cmd');
            end
        else
            set(handles.msg_display, 'String', 'Cannot send cmd. Comport not opened');
        end
    catch ME
        set(handles.msg_display, 'String', ME.message);
    end
    
%% --------------------------------
% CLK1 & CLK2
% ---------------------------------
% On the PCB are two chips that generate clocks and need controlling.
% clk1_val: a popupmenu with predefined values for clk1
% clk2_val: a popupmenu with predefined values for clk2
% clk1_set: a pushbutton to send a command to the LPC to set the value chosen for clk1_val
% clk2_set: a pushbutton to send a command to the LPC to set the value chosen for clk2_val
% ---------------------------------

% --- Executes on selection change in clk1_val.
function clk1_val_Callback(hObject, eventdata, handles)
% hObject    handle to clk1_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: contents = cellstr(get(hObject,'String')) returns clk1_val contents as cell array
%        contents{get(hObject,'Value')} returns selected item from clk1_val

% --- Executes during object creation, after setting all properties.
function clk1_val_CreateFcn(hObject, eventdata, handles)
% hObject    handle to clk1_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on selection change in clk2_val.
function clk2_val_Callback(hObject, eventdata, handles)
% hObject    handle to clk2_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: contents = cellstr(get(hObject,'String')) returns clk2_val contents as cell array
%        contents{get(hObject,'Value')} returns selected item from clk2_val

% --- Executes during object creation, after setting all properties.
function clk2_val_CreateFcn(hObject, ~, handles)
% hObject    handle to clk2_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in clk1_set.
function clk1_set_Callback(hObject, eventdata, handles)
% hObject    handle to clk1_set (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global clk_availfreq;
    i = get(handles.clk1_val, 'Value'); % get the value from the global list of available frequencies
    clk_sendcmd_set(handles, 1, clk_availfreq{i});

% --- Executes on button press in clk2_set.
function clk2_set_Callback(hObject, eventdata, handles)
% hObject    handle to clk2_set (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global clk_availfreq;
    i = get(handles.clk2_val, 'Value'); % get the value from the global list of available frequencies
    clk_sendcmd_set(handles, 2, clk_availfreq{i});
 
% Send the necessary commands over the com port
function clk_sendcmd_set(handles, clk, val)
    str = '';
    
    % When going from 'off' to a value, switch on the output of the chip
    if (clk == 1)
        if (strncmp(handles.clk1_prevval, 'off', 3) == 1)
            clk_sendcmd_enable(handles, 1, 1);
        end
    elseif (clk == 2)
        if (strncmp(handles.clk2_prevval, 'off', 3) == 1)
            clk_sendcmd_enable(handles, 2, 1);
        end
    end

    % Set the new value
    switch (val)
        case 'off'
            clk_sendcmd_enable(handles, clk, 0);
        case '25'
            str = sprintf('cap clksetpll %d 144 25  0 36  4', clk);
        case '30'
            str = sprintf('cap clksetpll %d 144 25  0 24  5', clk);
        case '35'
            str = sprintf('cap clksetpll %d 145 25 15 26  4', clk);
        case '40'
            str = sprintf('cap clksetpll %d 144 25  0 18  5', clk);
        case '45'
            str = sprintf('cap clksetpll %d 144 25  0 20  4', clk);
        case '50'
            str = sprintf('cap clksetpll %d 144 25  0 12  6', clk);
        case '55'
            str = sprintf('cap clksetpll %d 143 25  0 13  5', clk);
        case '60'
            str = sprintf('cap clksetpll %d 144 25  0 12  5', clk);
        case '65'
            str = sprintf('cap clksetpll %d 143 25  0 11  5', clk);
        case '70'
            str = sprintf('cap clksetpll %d 145 25 15 13  4', clk);
        case '75'
            str = sprintf('cap clksetpll %d 144 25  0  8  6', clk);
        case '80'
            str = sprintf('cap clksetpll %d 144 25  0  9  5', clk);
        case '85'
            str = sprintf('cap clksetpll %d 142 25 20  6  7', clk);
        case '90'
            str = sprintf('cap clksetpll %d 144 25  0  8  5', clk);
        case '100'
            str = sprintf('cap clksetpll %d 144 25  0  9  4', clk);
    end
    com_sendcmd(handles, str);
    
    % Calibrate the VCO
    if (clk == 1)
        clk_sendcmd_calibrateVco(handles, 1);
    elseif (clk == 2)
        clk_sendcmd_calibrateVco(handles, 2);
    end
        
    % Remember the value to allow switching on the chip when going from 'off' to value
    if (clk == 1)
        handles.clk1_prevval = val;
    elseif (clk == 2)
        handles.clk2_prevval = val;
    end
    guidata(handles.output, handles);
    pause(0.5);

function clk_sendcmd_calibrateVco(handles, clk)
    % Issue SPI controlled VCO calibration (Data Sheet page 17, Part initialization)
    % TODO: Here we should read register 0x0e and then make autoclearing bit 7 equal to 1
    % However, that involes making a wait loop here and get result from
    % comport callback. For now, I simply set the value of reg 0x0E to
    % 0xF4.
    str = sprintf('cap clkwritereg %d 0x0E 0x84', clk);
    com_sendcmd(handles, str);
    pause(0.5);
    str = sprintf('cap clkwritereg %d 0x05 0x01', clk);
    com_sendcmd(handles, str);
    pause(0.5);

function clk_sendcmd_enable(handles, clk, enable)
    str = '';
    if (enable == 1)
        % enable
        str = sprintf('cap clkwritereg %d 0x34 0x81', clk);
        com_sendcmd(handles, str);
    else
        % disable
        str = sprintf('cap clkwritereg %d 0x34 0xC1', clk);
        com_sendcmd(handles, str);
    end
    % I/O update
    str = sprintf('cap clkwritereg %d 0x05 0x01', clk);
    com_sendcmd(handles, str);
    pause(0.5);


%% --------------------------------
% DAC / POWER
% ---------------------------------
% On the PCB are four DACs that need controlling.
% dac_select: a popupmenu to select one of 4 DACs
% dac_value:  a edit to enter a new value for the specified DAC
% dac_set:    a pushbutton to send a command to the LPC to set the value for the chosen DAC
% ---------------------------------

% --- Executes on selection change in dac_select.
function dac_select_Callback(hObject, eventdata, handles)
% hObject    handle to dac_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: contents = cellstr(get(hObject,'String')) returns dac_select contents as cell array
%        contents{get(hObject,'Value')} returns selected item from dac_select

% --- Executes during object creation, after setting all properties.
function dac_select_CreateFcn(hObject, eventdata, handles)
% hObject    handle to dac_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function dac_value_Callback(hObject, eventdata, handles)
% hObject    handle to dac_value (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of dac_value as text
%        str2double(get(hObject,'String')) returns contents of dac_value as a double

% --- Executes during object creation, after setting all properties.
function dac_value_CreateFcn(hObject, eventdata, handles)
% hObject    handle to dac_value (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in dac_set.
function dac_set_Callback(hObject, eventdata, handles)
% hObject    handle to dac_set (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global dac_availdac;

    % Check if voltage is below max. Use the stored value and not the value
    % in dac_maxvalue. User can change dac_maxvalue but not press Set. If
    % that happens, the value in dac_maxvalue doesn't match 
    
    i = get(handles.dac_select, 'Value');     % index of the selected DAC in list of available DACs
    dac = lower(dac_availdac{i});             % string containing the selected DAC

    s_val = get(handles.dac_value, 'String');    % Get the string containing the new value
    s_maxval = get(handles.dac_maxvalue, 'String'); % Get the stored max value for this DAC
    val = str2double(s_val);
    maxval = str2double(s_maxval);
   
    if (val > maxval)
        set(handles.dac_value , 'String', s_maxval);
        set(handles.msg_display, 'String', 'Requested voltage higher than maximum. Voltage not changed.');
    else
        dac_sendcmd_setv(handles, dac, s_val);
    end

% Calculations assume Vdd of DAC is 3.3V.
function newval = dac_convert(v)
    vd = 4096 * v / 3.3;
    newval = dec2hex(round(vd));
    return;

% Both params are strings
function dac_sendcmd_setv(handles, which, val)
    vf = str2double(val); % from string to float
    vh = dac_convert(vf); % Convert new power to hexadecimal value
    % create command
    str = sprintf('cap setv %s 0x%s', which, vh);
    com_sendcmd(handles, str); % send command

% Both params are strings
function dac_sendcmd_setvmax(handles, which, val)
    vf = str2double(val); % from string to float
    vh = dac_convert(vf); % Convert new power to hexadecimal value
    % create command
    str = sprintf('cap setvmax %s 0x%s', which, vh);
    com_sendcmd(handles, str); % send command


%% --------------------------------
% POWER MAX values
% ---------------------------------
% dac_maxselect: a popupmenu to select one of 4 DACs
% dac_maxvalue:  a edit to enter a new value for the specified DAC
% dac_maxset:    a pushbutton to send a command to the LPC to set the maximum value for the chosen DAC
% ---------------------------------

% --- Executes on selection change in dac_maxselect.
function dac_maxselect_Callback(hObject, eventdata, handles)
% hObject    handle to dac_maxselect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: contents = cellstr(get(hObject,'String')) returns dac_maxselect contents as cell array
%        contents{get(hObject,'Value')} returns selected item from dac_maxselect

% --- Executes during object creation, after setting all properties.
function dac_maxselect_CreateFcn(hObject, eventdata, handles)
% hObject    handle to dac_maxselect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function dac_maxvalue_Callback(hObject, eventdata, handles)
% hObject    handle to dac_maxvalue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of dac_maxvalue as text
%        str2double(get(hObject,'String')) returns contents of dac_maxvalue as a double
    i = get(handles.dac_maxselect, 'Value');          % index of the selected DAC in list of available DACs
    handles.dac_maxval{i} = get(hObject, 'String');   % remember the new value
    set(hObject, 'String', handles.dac_maxvaltmp{i}); % write the previous value back. When the 'Set' button is clicked next, the new value will appear in the edittext.
    guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function dac_maxvalue_CreateFcn(hObject, eventdata, handles)
% hObject    handle to dac_maxvalue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in dac_maxset.
function dac_maxset_Callback(hObject, eventdata, handles)
% hObject    handle to dac_maxset (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global dac_availdac;
    
    % Get selected DAC
    i = get(handles.dac_maxselect, 'Value');   % index of the selected DAC in list of available DACs
    dac = lower(dac_availdac{i});              % string containing the selected DAC
    val = handles.dac_maxval{i};               % string containing the new value
    set(handles.dac_maxvalue, 'String', val);  % write the new value to the edit text.
    handles.dac_maxvaltmp{i} = val;            % Store new 'old' value 
    dac_sendcmd_setvmax(handles, dac, val);
    guidata(hObject, handles);

%% --------------------------------
% Command files
% ---------------------------------
% cmdfile_display: a edit that show the filename of the selected file
% cmdfile_select:  a pushbutton that displays a modal dialog box that lists files in the current folder and enables you to select or enter the name of a file
% cmdfile_execute: a pushbutton that starts execution of the selected file
% cmdfile_cancel:  a pushbutton to cancel execution of the selected file
% ---------------------------------

% --- Executes on button press in cmdfile_select.
function cmdfile_select_Callback(hObject, eventdata, handles)
% hObject    handle to cmdfile_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles.cmdfilename = uigetfile('*.txt');
    set(handles.cmdfile_display, 'String', handles.cmdfilename);
    guidata(hObject, handles);


% --- Executes on button press in cmdfile_execute.
function cmdfile_execute_Callback(hObject, eventdata, handles)
% hObject    handle to cmdfile_execute (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    set(hObject, 'Enable', 'off'); % Disable the execute button, so it can't be clicked twice
    set(handles.cmdfile_select, 'Enable', 'off'); % Disable the Select file button, so user can't select another file
    set(handles.cmdfile_cancel, 'Enable', 'on');  % Enable the cancel button

    % handles.cmdfilenameis the result of uigetfile. If the file name is
    % valid (and the file exists), uigetfile returns the file name as a
    % string when you click Open. If you click Cancel (or the window's close box),
    % uigetfile returns 0.
    if (handles.cmdfilename ~= 0)
        % open selected file
        handles.cmdfileID = fopen(handles.cmdfilename, 'r');
        if (handles.cmdfileID == -1)
            msg = sprintf('Failed to open cmdfile %s', handles.cmdfilename);
            set(handles.msg_display, 'String', msg);
        else
            msg = sprintf('Opened cmdfile %s', handles.cmdfilename);
            set(handles.msg_display, 'String', msg);
            
            % show hourglass
            oldpointer = get(handles.figure1, 'pointer');
            set(handles.figure1, 'pointer', 'watch');
            drawnow;
            
            % read line by line and execute the command
            line = fgetl(handles.cmdfileID);
            handles.line_number = 1;
            h = findobj('Tag', 'cmdfile_cancel');
            while ischar(line) % check if cline is a char. If EOF then fgetl returns -1.
                cmdfile_parseandexecute(handles, line);
                line = fgetl(handles.cmdfileID);
                handles.line_number = handles.line_number + 1;
                
                % Check if Cancel button is pressed
                data = get(h, 'UserData');
                if strcmp(data, 'STOP')
                    now = java.lang.System.currentTimeMillis; %http://practicalmatlab.com/
                    msg2 = sprintf('%d execute cancelled%s\n', now);
                    set(handles.msg_display, 'String', msg2);
                    fprintf(handles.logfileID, '%s\n', msg2);

                   	set(h, 'UserData', 'RUN');
                    break;
                end
            end

            % show original pointer
            set(handles.figure1, 'pointer', oldpointer);
            drawnow;
             
            % close the file
            fclose(handles.cmdfileID);
        end
     else
        set(handles.msg_display, 'String', 'No file selected');        
    end
    set(hObject, 'Enable', 'on'); % Enable the execute button
    set(handles.cmdfile_cancel, 'Enable', 'off'); % Disable the cancel button
    set(handles.cmdfile_select, 'Enable', 'on'); % Enable the Select file button
   
    guidata(hObject, handles);
    
% Commands
%   line starting with %  -> comments
%   wait <n>              -> wait for n seconds
%   #<n> d<delay> <cmd>   -> a command has to be executed n times.
%                            n is specified immediately after #
%                            next parameter is the delay between the consecutive commands in milliseconds
%                            e.g. #5 d10 cap readall
%   cap clk <sel> <val>   -> Simplified set clk command
%                            cap clk 1 25 -> set clk1 to 25 MHz
%                            cap clk 2 80 -> set clk2 to 80 MHz
%                            only predefined valid values: see clk_availfreq
%   cap setv <sel> <val>  -> Simplified setv command
%                            cap setv vddd 1.1 -> set vddd to 1.1 V
%   !<cmd>                -> sytem call
%   grab <filename>       -> start grabbing to given file. use data comport from GUI
%   Other commands as described in the LPC commandline interface are send
%   to LPC as is
function cmdfile_parseandexecute(handles, line)
    % Execute the command. Skip if first char on line is % -> comments
    % wait n -> wait for n seconds
    if (strncmpi(line, 'wait', 4) == 1) % wait for n seconds
        %display('--- wait for n seconds');
        [n, count, errmsg] = sscanf(line, 'wait %d');
        if (count ~= 1)
            if (isempty(errmsg))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        else
            max = n;
            % display a progress bar when more than 2 seconds wait
            if (max > 2)
                wb = waitbar(0, '1', 'Name','Waiting seconds...', 'CreateCancelBtn', 'setappdata(gcbf, ''canceling'' ,1)');
                setappdata(wb, 'canceling', 0);
            end
            h = findobj('Tag', 'cmdfile_cancel');
            while (n > 0)         
                if (max > 2)
                % Report current estimate in the waitbar's message field
                waitbar((max - n)/max, wb, sprintf('%d of %d', (max - n), max));
                end

                % execute the actual action, in this case PAUSE 1 second
                pause(1);
                n = n - 1;

                if (max > 2)ad
                    % Check if Cancel button in waitbar is pressed
                    if getappdata(wb, 'canceling')
                        n = 0;
                    end
                end
                % Check if Cancel button in CmdFile GUI part is pressed
                data = get(h, 'UserData');
                if strcmp(data, 'STOP')
                    n = 0;
                end
            end
            if (max > 2)
                delete(wb) % DELETE the waitbar; don't try to CLOSE it.
            end
        end
    elseif (strncmpi(line, '%', 1) == 1) % skip comment
%        display('--- Skip comment');

    elseif (strncmpi(line, '#', 1) == 1)
        % # indicates a command has to be executed n times. n is specified immediately after #
        % next parameter is the delay between the consecutive commands
        % java.lang.Thread.sleep(d); d in milliseconds
        % e.g. #5 d10 cap readall
        %display('--- REPEAT');
        [token, remain] = strtok(line);
        [n, count1, errmsg1] = sscanf(token, '#%d');
        max = n;
        [token, cmd] = strtok(remain);
        [d, count2, errmsg2] = sscanf(token, 'd%d');
         
        if (count1 ~= 1)
            if (isempty(errmsg1))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg1);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        elseif (count2 ~= 1)
            if (isempty(errmsg2))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg2);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        else
            wb = waitbar(0, '1', 'Name','Executing file. Please wait...', 'CreateCancelBtn', 'setappdata(gcbf, ''canceling'' ,1)');
            while (n > 0)    
                % Report current estimate in the waitbar's message field
                waitbar((max - n)/max, wb, sprintf('%d of %d', (max - n), max));

                % execute the actual action
                cmdfile_parseandexecute(handles, cmd);
                n = n - 1;

                java.lang.Thread.sleep(d);
                % Check if Cancel button in waitbar is pressed
                if getappdata(wb, 'canceling')
                    n = 0;
                end

                % Check if Cancel button is pressed
                h = findobj('Tag', 'cmdfile_cancel');
                data = get(h, 'UserData');
                if strcmp(data, 'STOP')
                    n = 0;
                end
            end
            delete(wb) % DELETE the waitbar; don't try to CLOSE it.
        end
    elseif (strncmpi(line, 'cap clk ', 8) == 1)
        % Simplified set clk command
        % cap clk 1 25  -> set clk1 to 25 MHz
        % cap clk 2 80  -> set clk2 to 80 MHz
        % cap clk 2 off -> clk2 off
        %display('--- set CLK');           
        [clk, count1, errmsg1] = sscanf(line, 'cap clk %s');
        tmp = ['cap clk ' clk ' %s'];
        [val, count2, errmsg2] = sscanf(line, tmp);
        if (count1 ~= 1)
            if (isempty(errmsg1))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg1);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        elseif (count2 ~= 1)
            if (isempty(errmsg2))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg2);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        else
            clk_sendcmd_set(handles, str2double(clk), val);
        end
    elseif (strncmpi(line, 'cap setv ', 9) == 1)
        % Simplified setv command
        % cap setv vddd 1.1 -> set vddd to 1.1 V
        %display('--- setv');
        [dac, count1, errmsg1] = sscanf(line, 'cap setv %s');
        tmp = ['cap setv ' dac ' %s'];
        [val, count2, errmsg2] = sscanf(line, tmp);
        if (count1 ~= 1)
            if (isempty(errmsg1))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg1);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        elseif (count2 ~= 1)
            if (isempty(errmsg2))
                msg = sprintf('Error at line %d: not enough parameters\n', handles.line_number);
            else
                msg = sprintf('Error at line %d: %s\n', handles.line_number, errmsg2);
            end
            set(handles.msg_display, 'String', msg);
            fprintf(handles.logfileID, '%s\r\n', sprintf('%d %s\n', java.lang.System.currentTimeMillis, msg));
        else
            dac_sendcmd_setv(handles, dac, val);
        end
    elseif (strncmpi(line, '!', 1) == 1)
        % sytem call
        [token, ~] = strtok(line, '!&');
        %display(token);
        % make sure that the program is started in the background
        tmp = sprintf('%s &\n', token);
        %display(tmp);
        system(tmp);
    elseif (strncmpi(line, 'grab', 4) == 1)
        % grab <filename>, use data comport from GUI
        display('Start grabbing');
        [~, remain] = strtok(line, ' ');
        % remain should not be empty!
        if (isempty(strtrim(remain)))
            set(handles.msg_display, 'String', 'Start grabbing failed: No destination file given');
            %display('empty filename');
        else
            cmd = sprintf('%s -c %s -o %s &\n', handles.css_datagrabber, handles.datacom_port, remain);
            system(cmd);
        end
    else
        % Other commands are as in the LPC commandline interface
        %execute command and wait 0.01 second
        %display('--- Other command');
        com_sendcmd(handles, line);
    end

function cmdfile_display_Callback(hObject, eventdata, handles)
% hObject    handle to cmdfile_display (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of cmdfile_display as text
%        str2double(get(hObject,'String')) returns contents of cmdfile_display as a double

% --- Executes during object creation, after setting all properties.
function cmdfile_display_CreateFcn(hObject, eventdata, handles)
% hObject    handle to cmdfile_display (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in cmdfile_cancel.
function cmdfile_cancel_Callback(hObject, eventdata, handles)
% hObject    handle to cmdfile_cancel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    set(hObject, 'UserData', 'STOP');

%% --------------------------------
% DEBUG
% ---------------------------------
% debug_select: a popupmenu with predefined values for debug
% debug_set:    a pushbutton to send a command to the LPC to set the value chosen for debug
% ---------------------------------

% --- Executes on selection change in debug_select.
function debug_select_Callback(hObject, eventdata, handles)
% hObject    handle to debug_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: contents = cellstr(get(hObject,'String')) returns debug_select contents as cell array
%        contents{get(hObject,'Value')} returns selected item from debug_select

% --- Executes during object creation, after setting all properties.
function debug_select_CreateFcn(hObject, eventdata, handles)
% hObject    handle to debug_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in debug_set.
function debug_set_Callback(hObject, eventdata, handles)
% hObject    handle to debug_set (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global debug_values;
    i = get(handles.debug_select, 'Value');
    display(i);
    cmd = sprintf('cap setdbglevel %d', debug_values{i, 2});
    display(cmd);
    com_sendcmd(handles, cmd);

    
%% --------------------------------
% READ ADC MANUAL
% ---------------------------------
% read_cmd:            a pushbutton to send the 'readall' command to the LPC
% read_result:         an edit to show the results of 'readall'
% ---------------------------------

% --- Executes on button press in read_cmd.
function read_cmd_Callback(hObject, eventdata, handles)
% hObject    handle to read_cmd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    cmd = 'cap readall';
    com_sendcmd(handles, cmd);

    function read_result_Callback(hObject, eventdata, handles)
% hObject    handle to read_result (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of read_result as text
%        str2double(get(hObject,'String')) returns contents of read_result as a double

% --- Executes during object creation, after setting all properties.
function read_result_CreateFcn(hObject, eventdata, handles)
% hObject    handle to read_result (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

%% --------------------------------
% CHIP CONFIG
% ---------------------------------
% chip_startstopones:   a togglebutton to start and stop sending '1' to the chip under test
% chip_startstopzeroes: a togglebutton to start and stop sending '0' to the chip under test
% chip_sendsingleone:   a pushbutton to send a single '1' to the chip under test
% chip_sendsinglezero:  a pushbutton to send a single '0' to the chip under test
% chip_sendnones:       a pushbutton to send <n> '1' to the chip under test
% chip_sendnzeroes:     a pushbutton to send <n> '0' to the chip under test
% chip_n:               an edit to enter <n>
% ---------------------------------

% --- Executes on button press in chip_startstopones.
function chip_startstopones_Callback(hObject, eventdata, handles)
% hObject    handle to chip_startstopones (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of chip_startstopones
    button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    if (button_state == max)  
        % toggle button is pressed, perform action1
        if (handles.com_opened)
            % disable the other buttons
            set(handles.chip_startstopzeroes, 'Enable', 'off');
            set(handles.chip_sendsingleone,   'Enable', 'off');
            set(handles.chip_sendsinglezero,  'Enable', 'off');
            set(handles.chip_sendnones,       'Enable', 'off');
            set(handles.chip_sendnzeroes,     'Enable', 'off');
            % send the command
            com_sendcmd(handles, 'cap capval 1');
            com_sendcmd(handles, 'cap capgo 1');
            % change the button String
            set(hObject, 'String', 'Stop sending 1');
        else
            set(hObject, 'Value', min); % toggle the button back
            set(handles.msg_display, 'String', 'Cannot send cmd. Comport not opened');
        end
    elseif (button_state == min)
        % toggle button is not pressed, perform action2
        if (handles.com_opened)
            % enable the other three buttons
            set(handles.chip_startstopzeroes, 'Enable', 'on');
            set(handles.chip_sendsingleone,   'Enable', 'on');
            set(handles.chip_sendsinglezero,  'Enable', 'on');
            set(handles.chip_sendnones,       'Enable', 'on');
            set(handles.chip_sendnzeroes,     'Enable', 'on');
            % send the command
            com_sendcmd(handles, 'cap capgo 0');
            % change the button String
            set(hObject, 'String', 'Start sending 1');
        else
            set(hObject, 'Value', max); % toggle the button back
            set(handles.msg_display, 'String', 'Cannot send cmd. Comport not opened');
        end
    end

% --- Executes on button press in chip_startstopzeroes.
function chip_startstopzeroes_Callback(hObject, eventdata, handles)
% hObject    handle to chip_startstopzeroes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of chip_startstopzeroes

    button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    if (button_state == max)
        % toggle button is pressed, perform action1
        if (handles.com_opened)
            % disable the other buttons
            set(handles.chip_startstopones,  'Enable', 'off');
            set(handles.chip_sendsingleone,  'Enable', 'off');
            set(handles.chip_sendsinglezero, 'Enable', 'off');
            set(handles.chip_sendnones,      'Enable', 'off');
            set(handles.chip_sendnzeroes,    'Enable', 'off');
            % send the command
            com_sendcmd(handles, 'cap capval 0');
            com_sendcmd(handles, 'cap capgo 1');
            % change button String
            set(hObject, 'String', 'Stop sending 0');
        else
            set(hObject, 'Value', min); % toggle the button back
            set(handles.msg_display, 'String', 'Cannot send cmd. Comport not opened');
        end

    elseif (button_state == min)
        % toggle button is not pressed, perform action2
        if (handles.com_opened)
            % enable the other buttons
            set(handles.chip_startstopones,  'Enable', 'on');
            set(handles.chip_sendsingleone,  'Enable', 'on');
            set(handles.chip_sendsinglezero, 'Enable', 'on');
            set(handles.chip_sendnones,      'Enable', 'on');
            set(handles.chip_sendnzeroes,    'Enable', 'on');
            % send the command
            com_sendcmd(handles, 'cap capgo 0');
            % change button String
            set(hObject, 'String', 'Start sending 0');
        else
            set(hObject, 'Value', max); % toggle the button back
            set(handles.msg_display, 'String', 'Cannot send cmd. Comport not opened');
        end
    end

% --- Executes on button press in chip_sendsingleone.
function chip_sendsingleone_Callback(hObject, ~, handles)
% hObject    handle to chip_sendsingleone (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of chip_sendsingleone
    com_sendcmd(handles, 'cap capregtest2 1 1');

% --- Executes on button press in chip_sendsinglezero.
function chip_sendsinglezero_Callback(hObject, eventdata, handles)
% hObject    handle to chip_sendsinglezero (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of chip_sendsinglezero
    com_sendcmd(handles, 'cap capregtest2 1 0');

% --- Executes on button press in chip_sendnones.
function chip_sendnones_Callback(hObject, eventdata, handles)
% hObject    handle to chip_sendnones (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    % read n
    n = get(handles.chip_n, 'String');
    % send command
    if (~isempty(n))
        cmd = sprintf('cap capregtest2 %s 1', n);
        com_sendcmd(handles, cmd);
    else
        set(handles.msg_display, 'String', 'Please enter value for n');
    end

% --- Executes on button press in chip_sendnzeroes.
function chip_sendnzeroes_Callback(hObject, eventdata, handles)
% hObject    handle to chip_sendnzeroes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    % read n
    n = get(handles.chip_n, 'String');
    % send command
    if (~isempty(n))
        cmd = sprintf('cap capregtest2 %s 0', n);
        com_sendcmd(handles, cmd);
    else
        set(handles.msg_display, 'String', 'Please enter value for n');
    end

function chip_n_Callback(hObject, eventdata, handles)
% hObject    handle to chip_n (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of chip_n as text
%        str2double(get(hObject,'String')) returns contents of chip_n as a double

% --- Executes during object creation, after setting all properties.
function chip_n_CreateFcn(hObject, eventdata, handles)
% hObject    handle to chip_n (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

%% --------------------------------
% READ ADC DMA
% ---------------------------------
% datacom_val:         edit to set the comport to read the data from
% datafile_val:        edit to set the name of the file to store the data
% t1_s0, t1_s1, t1_s2:    checkboxes to set the target configuration
% t2_s0, t2_s1, t2_s2:    checkboxes to set the target configuration
% nt_s0, nt_s1, nt_s2: checkboxes to set the non-target configuration
% cellconfiggroup:     radiobuttons to mutually exclusive select configuration 'single cell' or 'cell pair'
% dma_interval:        edit to enter the interval between 2 dma requests
% dma_interval_set:    pushbutton to send the dma interval value to the LPC
% start_data_read:     togglebutton to start/stop transfer of data from ADC, via LPC to comport using DMA
% ---------------------------------

function datacom_val_Callback(hObject, eventdata, handles)
% hObject    handle to datacom_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of datacom_val as text
%        str2double(get(hObject,'String')) returns contents of datacom_val as a double
% retrieve the number of the com port.
    gui_datacom = get(hObject, 'String');
    %display(gui_datacom);
    handles.datacom_port = sscanf(gui_datacom, 'COM%s'); %sscanf will search for 'COMx', where x is the number of the COM port (assuming that the user did comply to this format), and return x as a string (not as a number)
%BEGIN of "code added by Frans"
    if handles.datacom_s_exists
        delete(handles.datacom_s); %delete existing serial port object for data
    end
    handles.datacom_s_exists = false; %Frans: new serial port object for data need to be created and configured if port name changed
    guidata(hObject,handles); %Frans: added to store updated handles structure
%EEND of "code added by Frans"

    
% --- Executes during object creation, after setting all properties.
function datacom_val_CreateFcn(hObject, eventdata, handles)
% hObject    handle to datacom_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function datafile_val_Callback(hObject, eventdata, handles)
% hObject    handle to datafile_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of datafile_val as text
%        str2double(get(hObject,'String')) returns contents of datafile_val as a double

% --- Executes during object creation, after setting all properties.
function datafile_val_CreateFcn(hObject, eventdata, handles)
% hObject    handle to datafile_val (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in t1_s0.
function t1_s0_Callback(hObject, eventdata, handles)
% hObject    handle to t1_s0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of t1_s0

% --- Executes on button press in t1_s1.
function t1_s1_Callback(hObject, eventdata, handles)
% hObject    handle to t1_s1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of t1_s1

% --- Executes on button press in t1_s2.
function t1_s2_Callback(hObject, eventdata, handles)
% hObject    handle to t1_s2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of t1_s2

% --- Executes on button press in t2_s2.
function t2_s2_Callback(hObject, eventdata, handles)
% hObject    handle to t2_s2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of t2_s2


% --- Executes on button press in t2_s1.
function t2_s1_Callback(hObject, eventdata, handles)
% hObject    handle to t2_s1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of t2_s1

% --- Executes on button press in t2_s0.
function t2_s0_Callback(hObject, eventdata, handles)
% hObject    handle to t2_s0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of t2_s0

% --- Executes on button press in nt_s0.
function nt_s0_Callback(hObject, eventdata, handles)
% hObject    handle to nt_s0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of nt_s0

% --- Executes on button press in nt_s1.
function nt_s1_Callback(hObject, eventdata, handles)
% hObject    handle to nt_s1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of nt_s1

% --- Executes on button press in nt_s2.
function nt_s2_Callback(hObject, eventdata, handles)
% hObject    handle to nt_s2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of nt_s2

% --- Executes when selected object is changed in cellconfiggroup.
function cellconfiggroup_SelectionChangeFcn(hObject, eventdata, handles)
% hObject    handle to the selected object in cellconfiggroup 
% eventdata  structure with the following fields (see UIBUTTONGROUP)
%	EventName: string 'SelectionChanged' (read only)
%	OldValue: handle of the previously selected object or empty if none was selected
%	NewValue: handle of the currently selected object
% handles    structure with handles and user data (see GUIDATA)
if (eventdata.NewValue == handles.singlecell)
    set(handles.target2_panel, 'Visible', 'off');
else
    set(handles.target2_panel, 'Visible', 'on');
end

function dma_interval_Callback(hObject, eventdata, handles)
% hObject    handle to dma_interval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of dma_interval as text
%        str2double(get(hObject,'String')) returns contents of dma_interval as a double

% --- Executes during object creation, after setting all properties.
function dma_interval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to dma_interval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in dma_interval_set.
function dma_interval_set_Callback(hObject, eventdata, handles)
% hObject    handle to dma_interval_set (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    i = get(handles.dma_interval, 'String');
    %display(i);
    cmd = sprintf('cap dmaint %s', i);
    com_sendcmd(handles, cmd);

    % --- Executes on button press in start_data_read.
function start_data_read_Callback(hObject, eventdata, handles)
% hObject    handle to start_data_read (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    % At startup, button_state is set to 'Max'.
    

    selectedRadiobuttonTag = get(handles.cellconfiggroup, 'SelectedObject');
    


    %pause(1e-100);
     guidata(hObject,handles);
     lockstatus=handles.stlockstatus;
     guidata(hObject,handles);

if lockstatus==0 || isempty(lockstatus)==1;
    display('Please first lock the signal trace mark');
    msgbox('Please first lock the signal trace mark','warning','error')
else
    if (button_state == max)

        try
            handles.SamplesReference = zeros(3,1024); %create handle for reference samples of selected channels, and initializeto zero
            slider3_Callback(handles.slider3, 0, handles); %initialize warped weight factors
            handles=guidata(handles.slider3); %get most recent version of handles (may have changed by previous call of function slider3_Callback)
            %open output file for data:
            handles.dataout = fopen(get(handles.datafile_val, 'String'),'w'); %use most recent version of output file for data (user may have changed it)
            %create and configure serial port object for data if not existing:
            if ~handles.datacom_s_exists
                handles.datacom_s = serial(sprintf('COM%s',handles.datacom_port)); %create serial port object for data, using most recent port number (updated by datacom_val_Callback if user changes port number in datacom_val field)
                handles.datacom_s.Baudrate = 115200;
                handles.datacom_s.DataBits = 8;
                handles.datacom_s.Parity = 'none';
                handles.datacom_s.StopBits = 1;
                handles.datacom_s.RequestToSend = 'off';
                handles.datacom_s.Timeout = 10; %check if this value works well under all circumstances!
                handles.datacom_s.InputBufferSize = 12292;
                handles.datacom_s.BytesAvailableFcnMode = 'byte';
                handles.datacom_s.BytesAvailableFcnCount = 12292; %4 bytes for packet number + 1024 * 12 bytes for packet data
                handles.datacom_s.BytesAvailableFcn = {@DataPortBytesAvailableHandler,handles}; %pass additional argument handles
                handles.datacom_s.ErrorFcn = {@DataPortErrorHandler,handles}; %not sure if an error handling function is necessary
                handles.datacom_s_exists = true; %conhandles.Images(nA)d serial port object for data exists and can be reused next time
           
            end

            %record_state=handles.record_state;



            
            %Delete decoded packet from previous run:
            %handles.packet.Number = []; %currently not used
            %handles.packet.Timestamp = []; %currently not used
            %handles.packet.Samples = []; %currently not used
            
            handles.datacom_s.UserData.CaptureData = true; %tell DataPortBytesAvailableHandler to capture 
            fopen(handles.datacom_s); %open serial port for data
            
            handles.tLast = now; %record time for calculating elapsed time between successive serial port callbacks
            


 %added by Tao
%  global datavoltage
%  global packetNumber
%  eval(['data_v',num2string(packetNumber),'=','datavoltage']);
 %end of code added by Tao 
                
        
        catch err_StartRead
            display(err_StartRead)
        end






    set(handles.start_data_read, 'String', 'Stop Read');

        
        % First get the target and non-target S0, S1 and S2 and send to LPC
        % if 'singe cell' is selected, then use 
        % 'cap confcell_s <t1_s0><t1_s1><t1_s2><nt_s0><nt_s1><nt_s2>'
        % if 'cell pair' is selected, use
        % 'cap confcell_p <t1_s0><t1_s1><t1_s2><t2_s0><t2_s1><t2_s2><nt_s0><nt_s1><nt_s2>'
        if (selectedRadiobuttonTag == handles.singlecell)
            cmd = 'cap confcell_s';
        else
            cmd = 'cap confcell_p';
        end
        
        % TARGET 1 : -> always add to command
        if (get(handles.t1_s0, 'Value') == get(handles.t1_s0, 'Max'))
            cmd = strcat(cmd, ' 1');
        else
            cmd = strcat(cmd, ' 0');
        end
        if (get(handles.t1_s1, 'Value') == get(handles.t1_s1, 'Max'))
            cmd = strcat(cmd, ' 1');
        else
            cmd = strcat(cmd, ' 0');
        end
        if (get(handles.t1_s2, 'Value') == get(handles.t1_s2, 'Max'))
            cmd = strcat(cmd, ' 1');
        else
            cmd = strcat(cmd, ' 0');
        end
        % TARGET 2 : -> only add when cell pair selected
        if (selectedRadiobuttonTag == handles.cellpair)
            if (get(handles.t2_s0, 'Value') == get(handles.t2_s0, 'Max'))
                cmd = strcat(cmd, ' 1');
            else
                cmd = strcat(cmd, ' 0');
            end
            if (get(handles.t2_s1, 'Value') == get(handles.t2_s1, 'Max'))
                cmd = strcat(cmd, ' 1');
            else
                cmd = strcat(cmd, ' 0');
            end
            if (get(handles.t2_s2, 'Value') == get(handles.t2_s2, 'Max'))
                cmd = strcat(cmd, ' 1');
            else
                cmd = strcat(cmd, ' 0');
            end
        end
        % NON-TARGET : -> always add to command
        if (get(handles.nt_s0, 'Value') == get(handles.nt_s0, 'Max'))
            cmd = strcat(cmd, ' 1');
        else
            cmd = strcat(cmd, ' 0');
        end
        if (get(handles.nt_s1, 'Value') == get(handles.nt_s1, 'Max'))
            cmd = strcat(cmd, ' 1');
        else
            cmd = strcat(cmd, ' 0');
        end
        if (get(handles.nt_s2, 'Value') == get(handles.nt_s2, 'Max'))
            cmd = strcat(cmd, ' 1');
        else
            cmd = strcat(cmd, ' 0');
        end
        com_sendcmd(handles, cmd);

        % Then start reading
       % cmd = 'cap startread';
        %now replaced by Tao
        
        cmd = 'cap 777';
        com_sendcmd(handles, cmd);
        
%{
        if (selectedRadiobuttonTag == handles.singlecell)
            cmd = strcat(cmd, ' s');
        else
            cmd = strcat(cmd, ' p');
        end
        com_sendcmd(handles, cmd);
%}

%end of code added by Tao  
    
 %added by Tao
%  global datavoltage
%  datavoltage=Samples;
%eval([writematrix,'(Samples',',','myData_',num2str(packetNumber),'.dat',',','Delimiter',',',';)']);
% writematrix(0,'myData.dat','Delimiter','tab')  
% type myData.dat
  %end of code added by Tao   

% BEGIN of "code added by Frans"
       
% END of "code added by Frans"


            % END of "code added by Frans"
    %        end



%end of code added by Tao   




elseif (button_state == min)
        set(handles.start_data_read, 'String', 'Start Read');
        %cmd = 'cap stopread';
        %now replaced by Tao
        cmd = 'cap 888';
        com_sendcmd(handles, cmd);

% BEGIN of "code added by Frans"
        try
            handles.datacom_s.UserData.CaptureData = false; %tell DataPortBytesAvailableHandler to not capture data anymore
            fclose(handles.dataout); %close output file for data
            fclose(handles.datacom_s);  %close serial port for data
        catch err_StopRead
            display(err_StopRead);
        end
% END of "code added by Frans"
end
    %Added by Frans:
    guidata(hObject, handles); %store modified handles

%% --------------------------------
% MESSAGES TO USER
% ---------------------------------
% msg_display: edit to show all message from the system to the user
end
% ---------------------------------

function msg_display_Callback(hObject, eventdata, handles)
% hObject    handle to msg_display (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of msg_display as text
%        str2double(get(hObject,'String')) returns contents of msg_display as a double

% --- Executes during object creation, after setting all properties.
function msg_display_CreateFcn(hObject, eventdata, handles)
% hObject    handle to msg_display (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in init_button.
function init_button_Callback(hObject, eventdata, handles)
% hObject    handle to init_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% disable the button
set(hObject, 'Enable', 'off');
%---------------------------------


 %code added by Tao
        %pre-allocate for video record
                %handles.record_state=0;       %presetting of start_record button state
                
%                 path = ['experiment', i_foldername];
%                 cd(path);
% 
%                 v=VideoWriter('guide.avi','Uncompressed AVI');
%                 v.FrameRate=5;
% %                 v.Quality=100;
%                 
% %                 cd('..');
%                 
%                 handles.video=v;
        %code added by Tao ended







% Read defaults from the ini file
% Set the default value in the GUI
% Set the default value in the LPC
%---------------------------------
set(handles.msg_display, 'String', 'Reading ini file'); pause(0.5);
handles.inifile = 'cssgui.ini';
if ~exist(handles.inifile, 'file')
    set(handles.msg_display, 'String', sprintf('File %s does not exist\n', handles.inifile));
    set(hObject, 'Enable', 'on');
    return;
end

%----
% LOG
%----
% Do this first. The automatic open of the com port needs the log file!
% Open log file to store commands

% Read defaults from the ini file
readKeys = { 'measurements', 'data', 'path', '', ''; };
measurements_datakeys = inifile(handles.inifile, 'read', readKeys);
handles.data_path = measurements_datakeys{1};
% Check if destination path exists
if ~exist(measurements_datakeys{1}, 'dir')
    set(handles.msg_display, 'String', sprintf('Destination directory %s does not exist\n', measurements_datakeys{1}));
    set(hObject, 'Enable', 'on');
    return;
end



logfilename = sprintf('%s\\mylogfile.txt', measurements_datakeys{1}); %Frans: sets default log file to path\mylogfile.txt with path defined in [measurements] section of cssgui.ini
outfilename = sprintf('%s\\myoutfile.txt', measurements_datakeys{1}); %Frans: sets default out file to path\myoutfile.txt with path defined in [measurements] section of cssgui.ini

% Set the default value in the GUI
handles.logfileID = fopen(logfilename, 'w');
if (handles.logfileID == -1)
    set(handles.msg_display, 'String', 'Failed to open logfile');
end
handles.outfileID = fopen(outfilename, 'w');
if (handles.outfileID == -1)
    set(handles.msg_display, 'String', 'Failed to open outputfile');
end

%------
% TOOLS
%------
readKeys = { 'measurements', 'tools', 'grabberpath', '', ''; };
toolskeys = inifile(handles.inifile, 'read', readKeys);
handles.css_datagrabber = sprintf('%s\\css_datagrabber.exe', toolskeys{1});
% Check if css_datagrabber path exists

%{
if ~exist(handles.css_datagrabber, 'file')
    set(handles.msg_display, 'String', sprintf('%s does not exist\n', handles.css_datagrabber));
    set(hObject, 'Enable', 'on');
    return;
end
%}

readKeys = { 'measurements', 'tools', 'checkerpath', '', ''; };
toolskeys = inifile(handles.inifile, 'read', readKeys);

%---------
% COM PORT
%---------
% Read defaults from the ini file
readKeys = { 'default', 'com', 'port', '', '7'; };
default_comkeys  = inifile(handles.inifile, 'read', readKeys);
handles.com_port = sprintf('COM%s', default_comkeys{1}); % Get the default value from the ini file
% Set the default value in the GUI
set(handles.com_val, 'String', handles.com_port);
handles.s = 0; % handle to the serial port
handles.com_opened = false; % remember if the comport was opened to give message when close button is pressed
set(handles.com_panel, 'Visible', 'on');

% Open the comport
cmd_com_open_Callback(handles.cmd_com_open, 0, handles);
%Frans: get the most recent version of handles:
handles = guidata(handles.cmd_com_open); % http://de.mathworks.com/matlabcentral/newsreader/view_thread/320742, message 9!

%----
% CLK
%----
set(handles.msg_display, 'String', 'Init clocks'); pause(0.5);
% Read defaults from the ini file
readKeys = { 'default', 'clk', 'clk1', '', '40';...
             'default', 'clk', 'clk2', '', '40';};
default_clkkeys  = inifile(handles.inifile, 'read', readKeys);
% Set the default value in the GUI
% Find the index of the default value in handles.clk_availfreq
global clk_availfreq;
tmp1 = find(strcmp(default_clkkeys{1}, clk_availfreq));
tmp2 = find(strcmp(default_clkkeys{2}, clk_availfreq));
set(handles.clk1_val, 'Value', tmp1);
set(handles.clk2_val, 'Value', tmp2);
handles.clk1_prevval = handles.clk1_val; 
handles.clk2_prevval = handles.clk2_val;
set(handles.clk_panel, 'Visible', 'on');
% Set the default value in LPC
clk1_set_Callback(handles.clk1_set, 0, handles); pause(0.5);
clk2_set_Callback(handles.clk2_set, 0, handles); pause(0.5);
set(handles.msg_display, 'String', 'Init clocks done'); pause(0.5);

%----
% DAC
%----
set(handles.msg_display, 'String', 'Init DACs'); pause(0.5);
% Read defaults from the ini file
readKeys = { 'default', 'dac', 'vddd',  '', '1.1';...
             'default', 'dac', 'vdda',  '', '1.1';...
             'default', 'dac', 'vcfi',  '', '0.9';...
             'default', 'dac', 'vbias', '', '0.5';};
default_dackeys  = inifile(handles.inifile, 'read', readKeys);
% Set the default value in the GUI
global dac_availdac;
set(handles.dac_select, 'String', dac_availdac);
set(handles.dac_maxselect, 'String', dac_availdac);
set(handles.dac_panel, 'Visible', 'on');
set(handles.dac_maxpanel, 'Visible', 'on');
% Keep 'old' value of dac_maxvalue edittext in dac_maxvaltmp. When leaving
% dac_maxvalue edit box, write new value in dac_maxval. Also write the old
% value back in the edittext. When you then click set, put the new value in
% the edit text. This gives weird behaviour if you don't clikc 'Sset'
% immediately after changing the value. However, this is typical flow.
handles.dac_maxval = {'1.1' '1.1' '1.1' '1.1'}; % max values for the DACs Vddd Vdda Vcfi and Vbias respectively
handles.dac_maxvaltmp = {'1.1' '1.1' '1.1' '1.1'}; % temporay max values for the DACs. When leaving editfield, write 
% Set the default value in LPC
dac_sendcmd_setv(handles, 'vddd',  default_dackeys{1}); pause(0.5);
dac_sendcmd_setv(handles, 'vdda',  default_dackeys{2}); pause(0.5);
dac_sendcmd_setv(handles, 'vcfi',  default_dackeys{3}); pause(0.5);
dac_sendcmd_setv(handles, 'vbias', default_dackeys{4}); pause(0.5);
set(handles.msg_display, 'String', 'Init DACs done'); pause(0.5);

%---------
% CMD FILE
%---------
handles.cmdfilename = 0;
set(handles.cmdfile_cancel, 'Enable', 'off');
set(handles.cmdfile_cancel, 'UserData', 'RUN');
set(handles.cmdfile_panel, 'Visible', 'on');

%------
% DEBUG
%------
global debug_values;
set(handles.debug_select, 'String', debug_values(1:7, 1));
set(handles.debug_select, 'Value', 5);
set(handles.debug_panel, 'Visible', 'on');


%------
% Notes and setting information
%------
set(handles.notes_panel, 'Visible', 'on');
set(handles.settings_panel, 'Visible', 'on');



%-----
% DATA
%-----
set(handles.msg_display, 'String', 'Init data'); pause(0.5);
% Read defaults from the ini file
readKeys = { 'default', 'data', 'datafile', '', 'outfile.dat';...
             'default', 'data', 'port',     '', '26';};
default_datakeys = inifile(handles.inifile, 'read', readKeys);
readKeys = { 'default', 'dma', 'interval', '', '80'; };
default_dmakeys = inifile(handles.inifile, 'read', readKeys);

set(handles.t1_s0, 'Value', get(handles.t1_s0, 'Min'));
set(handles.t1_s1, 'Value', get(handles.t1_s1, 'Min'));
set(handles.t1_s2, 'Value', get(handles.t1_s2, 'Min'));
set(handles.t2_s0, 'Value', get(handles.t2_s0, 'Min'));
set(handles.t2_s1, 'Value', get(handles.t2_s1, 'Min'));
set(handles.t2_s2, 'Value', get(handles.t2_s2, 'Min'));
set(handles.nt_s0, 'Value', get(handles.nt_s0, 'Min'));
set(handles.nt_s1, 'Value', get(handles.nt_s1, 'Min'));
set(handles.nt_s2, 'Value', get(handles.nt_s2, 'Min'));
% Default is single cell, hence target2_panel invisible
set(handles.singlecell, 'Value', get(handles.singlecell, 'Max'));
set(handles.target2_panel, 'Visible', 'off');

set(handles.start_data_read, 'Enable', 'on');
% Set the default value in the GUI
set(handles.datafile_val, 'String', sprintf('%s\\%s',handles.data_path,default_datakeys{1})); %Frans: data file name including full path
handles.datacom_port = default_datakeys{2}; % Get the default value from the ini file
set(handles.datacom_val, 'String', sprintf('COM%s', default_datakeys{2}));
set(handles.dma_interval, 'String', default_dmakeys{1});
set(handles.datamanual_panel, 'Visible', 'on');
set(handles.datadma_panel, 'Visible', 'on');
% Set the defaults in LPC
com_sendcmd(handles, sprintf('cap dmaint %s', default_dmakeys{1})); pause(0.5);

%code added by Tao
handles.stlockstatus=0;
     handles.x1=0; %pre-set handles for signal trace initial value
     handles.x2=0;
     handles.x3=0;
     handles.X1=[];
     handles.X2=[];
     handles.X3=[];
     handles.Y11=[];
     handles.Y12=[];
     handles.Y13=[];
     handles.Y14=[];
     handles.Y15=[];
     handles.Y21=[];
     handles.Y22=[];
     handles.Y23=[];
     handles.Y24=[];
     handles.Y25=[];
     handles.Y31=[];
     handles.Y32=[];
     handles.Y33=[];
     handles.Y34=[];
     handles.Y35=[];
%code added by Tao ended

%BEGIN of "code added by Frans"

handles.datacom_s_exists = false; %remember if serial object for data has been created
%Create handles to store decoded packet data. Make sure they exists even
%before first data is captured, so that they can be tested by processing
%functions:
%handles.packet.Number = []; %currently not used
%handles.packet.Timestamp = []; %currently not used
%handles.packet.Samples = []; %currently not used

%Physical sensing field parameters (row index: array number):
handles.SensingFields.Name = {'SensorMatrix'; 'SensorMatrix10um5x5';'SensorMatrix10um4x4'}; %array names
handles.SensingFields.a = [14.98; 9.8; 9.8]; %physical electrode pitch in a row (microns)
handles.SensingFields.b = [25.2; 15.12; 15.12]; %physical row pitch in a sub-array (microns)
handles.SensingFields.a1 = [7.5; 4.39; 4.39]; %physical offset of even to odd sub-grid, measured parallel to rows (microns)
handles.SensingFields.b1 = [12.6; 7.56; 7.56]; %physical offset of even to odd sub-grid, measured perpendicular to rows (microns)
handles.SensingFields.K = [32; 32; 32]; %number of electrodes per row
handles.SensingFields.L = [16; 16; 16]; %number of rows per sub-grid

%Displaying parameters (row index: array number, column index: available resolution):
handles.SensingFields.M = [6,12,26,32,38,44,50; 9,13,22,35,40,49,58; 9,13,22,35,40,49,58]; %number of pixels per electrode pitch in a row
handles.SensingFields.N = [10,20,44,54,64,74,84; 14,20,34,54,62,76,90; 14,20,34,54,62,76,90]; %number of pixels per row pitch in a sub-grid
handles.SensingFields.M1 = [3,6,13,16,19,22,25; 4,6,10,16,18,22,26; 4,6,10,16,18,22,26]; %number of pixels offset of even to odd sub-grid, measured parallel to rows
handles.SensingFields.N1 = [5,10,22,27,32,37,42; 7,10,17,27,31,38,45; 7,10,17,27,31,38,45]; %number of pixels offset of even to odd sub-grid, measured perpendicular to rows
handles.SensingFields.Resolution = [1; 1; 1]; %default resolution column indices

%Additional parameters for plotting:
handles.ConfidenceFactor = [3.6; 3.6; 3.6]; %upper/lower limits w.r.t mean divided by standard deviation (used for calculating plotting limits)
handles.Histograms.NumberOfVerticalTickmarks = [6; 6; 6]; %only used for rounding purposes; may differ in actual plots

%Create window for displaying sensor data:
handles.SensorData = figure('NumberTitle', 'off', 'Name', 'Sensor data', 'Menubar', 'none'); %create figure with default background color

NumberOfSensingFields = size(handles.SensingFields.Name,1);
W = cell(NumberOfSensingFields,3); %preallocate empty cell array
for nA = 1:NumberOfSensingFields
    %Initialize bitmap images:
    a = handles.SensingFields.a(nA);
    b = handles.SensingFields.b(nA);
    a1 = handles.SensingFields.a1(nA);
    b1 = handles.SensingFields.b1(nA);
    K = handles.SensingFields.K(nA);
    L = handles.SensingFields.L(nA);
    nR = handles.SensingFields.Resolution(nA);
    M = handles.SensingFields.M(nA,nR);
    N = handles.SensingFields.N(nA,nR);
    M1 = handles.SensingFields.M1(nA,nR);
    N1 = handles.SensingFields.N1(nA,nR);
    SensingFieldLength = (K+1)*a+a1; %physical length of sensing field, measured parallel to rows 
    SensingFieldWidth = (L+1)*b-b1; %physical width of sensing field, measured perpendicular to rows
    dx = SensingFieldLength/((K+1)*M+M1); %physical X-dimension associated with 1 pixel
    dy = SensingFieldWidth/((L+1)*N-N1); %physical Y-dimension associated with 1 pixel
 %>>handles.SubPlots(nA) = subplot(3,3,[nA,3+nA]); %combine 2 vertically stacked subplots for displaying a sensing field
    handles.SubPlots(nA) = subplot(4,3,[nA,3+nA]);
    handles.Images(nA) = imagesc([0.5*dy,SensingFieldWidth-0.5*dy],[SensingFieldLength-0.5*dx,0.5*dx],zeros((L+1)*N-N1,M1+(K+1)*M)); %create handels to bitmap images (used for fast updating of bitmaps)
    axis image; %make aspect ratio of the axes the same as the image
    title(handles.SensingFields.Name(nA)); %add title
    xlabel('X (\mum)'); ylabel('Y (\mum)'); % add axis labels
    axis manual;
    
    %code added by Tao
    hold on
%     handles.markimage1(nA)=line([a,1.089+5.32],[a+a1,a+a1],'color','r','linewidth',1);
%     handles.markimage2(nA)=line([a,1.089+5.32],[2a+a1,2a+a1],'color','r','linewidth',1);
%     handles.markimage3(nA)=line([1.089,1.089+5.32],[1.089,1.089],'color','r','linewidth',1);
%     handles.markimage4(nA)=line([1.089,1.089+5.32],[1.089,1.089],'color','r','linewidth',1);
%     handles.markimage5(nA)=line([1.089,1.089+5.32],[1.089,1.089],'color','r','linewidth',1);
%     handles.markimage6(nA)=line([1.089,1.089+5.32],[1.089,1.089],'color','r','linewidth',1);

%     handles.markimage1(nA)=line([0,b],[a,a],'color','r','linewidth',1);
%     handles.markimage2(nA)=line([0,b],[2*a,2*a],'color','r','linewidth',1);
%     handles.markimage3(nA)=line([0,0],[a,2*a],'color','r','linewidth',1);
%     handles.markimage4(nA)=line([b,b],[a,2*a],'color','r','linewidth',1);

    handles.markimage1(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','k');
    handles.markimage2(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','k');
    handles.markimage3(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','k');
    handles.markimage4(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','k');
    
    handles.markimage5(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','r');
    handles.markimage6(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','r');
    handles.markimage7(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','r');
    handles.markimage8(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','r');

    handles.markimage9(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','g');
    handles.markimage10(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','g');
    handles.markimage11(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','g');
    handles.markimage12(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','g');

    handles.markimage13(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','m');
    handles.markimage14(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','m');
    handles.markimage15(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','m');
    handles.markimage16(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','m');

    handles.markimage17(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','c');
    handles.markimage18(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','c');
    handles.markimage19(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','c');
    handles.markimage20(nA)=line([-1,-1],[-2,-1],'linewidth',1,'color','c');


    %handles.markimage(nA)=nsidedpoly()
    hold off;
    %handles.markimage(nA)=line([-1,-1],[-2,-1]);
    colorbar;
    %code added by Tao ended


    %Initialize cumulative distribution function (CDF) plots:
    XLim = [1600,2400]; %initial X-axis range of CDF plots
 %>>handles.SubPlots(3+nA) = subplot(3,3,6+nA,'XLim',XLim,'YLim',[0,1]); %create handles to CDF plots
    handles.SubPlots(3+nA) = subplot(4,3,6+nA,'XLim',XLim,'YLim',[0,1]); %create handles to CDF plots
    set(get(handles.SubPlots(3+nA),'XLabel'),'String','ADC code');
    set(get(handles.SubPlots(3+nA),'YLabel'),'String','Cumulative probability');
    handles.CDF_Plot(nA) = line(XLim,[0,0]); %create handles to function lines in CDF plots (used for fast updating of CDF plots)
 
%BEGIN EXPERIMENTAL SECTION
    %Initiallize signal trace plots:
    XLim = [0,0.01]; %initial X-axis range of signal trace plots
    handles.SubPlots(6+nA) = subplot(4,3,9+nA,'XLim',XLim,'YLim',[0,4095]); %create handles to signal trace plots
    set(get(handles.SubPlots(6+nA),'XLabel'),'String','Time (s)');
    set(get(handles.SubPlots(6+nA),'YLabel'),'String','ADC code');
    handles.SignalTracePlot1(nA) = line(XLim,[0,0],'color','k'); %create handles to function lines in signal trace plots (used for fast updating of CDF plots)
    %code added by Tao
     handles.SignalTracePlot2(nA) = line(XLim,[0,0],'color','r');
     handles.SignalTracePlot3(nA) = line(XLim,[0,0],'color','g');
     handles.SignalTracePlot4(nA) = line(XLim,[0,0],'color','m');
     handles.SignalTracePlot5(nA) = line(XLim,[0,0],'color','c');
     
     %legend('M1','M2','M3','M4','M5');
    


   %code added by Tao ended





    handles.Mask_Reference = zeros(6,1024); %preallocation and create handle to mask
    handles.Mask_Sense = zeros(6,1024); %preallocation and create handle to mask



 
%END EXPERIMENTAL SECTION

    %Interpolation weights:
    [W0,W1,W2] = WeightsLinear(M, N, M1, N1); %calulate linear interpolation weights
    W(nA,:) = {W0,W1,W2};
    
    %Time measurement:
    handles.tLast = now;
end
handles.Interpolation.WeightsLinear = W;

%END of "code added by Frans"

set(handles.msg_display, 'String', 'Init data done'); pause(0.5);

set(handles.msg_display, 'String', 'Init done');

guidata(hObject, handles);

% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: delete(hObject) closes the figure
if ~isempty(instrfind)
    fclose(instrfind); %Frans: close remaining open serial ports
    delete(instrfind); %Frans: delete remaining serial port objects
end
delete(hObject);


% --- Executes on slider movement.
function slider3_Callback(hObject, eventdata, handles)
% hObject    handle to slider3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

NumberOfSensingFields = size(handles.SensingFields.Name,1);
KernelMatricesOdd = cell(NumberOfSensingFields,1); %preallocate empty cell array
KernelMatricesEven = cell(NumberOfSensingFields,1); %preallocate empty cell array
Value = get(hObject,'Value');
if Value==0
    %Interpolated signal mode:
    KernelMatricesOdd = handles.Interpolation.WeightsLinear(1:NumberOfSensingFields,1); %(W0 matrices)
    for nA =1:NumberOfSensingFields
        KernelMatricesEven{nA} = rot90(KernelMatricesOdd{nA},2);
    end
elseif Value==1
    %Electrode signals mode:
    for nA = 1:NumberOfSensingFields
        nR = handles.SensingFields.Resolution(nA); %current resolution
        M = handles.SensingFields.M(nA,nR);
        N = handles.SensingFields.N(nA,nR);
        W0 = handles.Interpolation.WeightsLinear{nA,1};
%target        &change made by Tao (delete target), why target written here
        W1 = handles.Interpolation.WeightsLinear{nA,2};
        W2 = handles.Interpolation.WeightsLinear{nA,3};
        KernelMatrixOdd = zeros(2*M,N); %preallocation
        for i=1:2*M
            for j=1:N
                if W0(i,j)==0
                    KernelMatrixOdd(i,j) = 0;
                elseif single(W0(i,j))>single(max(W1(i,j),W2(i,j))) %single-precision comparison for robustness against errors in double precision numbers
                    KernelMatrixOdd(i,j) = 1;
                elseif single(W0(i,j))==single(max(W1(i,j),W2(i,j))) && W1(i,j)~=W2(i,j) %single-precision comparison for robustness against errors in double precision numbers
                    KernelMatrixOdd(i,j) = 1/2;
%               elseif W0(i,j)==W1(i,j) && W0(i,j)==W2(i,j)
%                   KernelMatrixOdd(i,j) = 1/3;
%This test for this special case is skipped (for speed reasons) because it
%cannot occur for integer points coordinates combined with half-integer
%evaluation grid coordinates (as used here). The commented code is only
%retained for completeness.
                else
                    KernelMatrixOdd(i,j) = 0;
                end
            end
        end
        KernelMatricesOdd{nA} = KernelMatrixOdd;
        KernelMatricesEven{nA} = rot90(KernelMatrixOdd,2);
    end
else
    %Intermediate mode:
    Gamma = 1/(1-Value);
    for nA = 1:NumberOfSensingFields
        nR = handles.SensingFields.Resolution(nA); %current resolution
        M = handles.SensingFields.M(nA,nR);
        N = handles.SensingFields.N(nA,nR);
        W0 = handles.Interpolation.WeightsLinear{nA,1};
        W1 = handles.Interpolation.WeightsLinear{nA,2};
        W2 = handles.Interpolation.WeightsLinear{nA,3};
        KernelMatrixOdd = zeros(2*M,N); %preallocation
        for i=1:2*M
            for j=1:N
                if W0(i,j)==0
                    KernelMatrixOdd(i,j) = 0; %initialization
                else
                    KernelMatrixOdd(i,j) = W0(i,j)^Gamma/(W0(i,j)^Gamma + W1(i,j)^Gamma + W2(i,j)^Gamma); %initialization
                end
            end
        end
        KernelMatricesOdd{nA} = KernelMatrixOdd;
        KernelMatricesEven{nA} = rot90(KernelMatrixOdd,2);
    end
end
handles.Interpolation.KernelMatricesOdd = KernelMatricesOdd;
handles.Interpolation.KernelMatricesEven = KernelMatricesEven;

%figure(handles.SensorData);
%for nA = 1:NumberOfSensingFields
%    set(handles.ConvolutionKernels(nA),'CData',KernelMatricesOdd{nA});
%end

guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function slider3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on key press with focus on start_data_read and none of its controls.
function start_data_read_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to start_data_read (see GCBO)
% eventdata  structure with the following fields (see UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in AutoScale.
function AutoScale_Callback(hObject, eventdata, handles)
% hObject    handle to AutoScale (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of 


% --- Executes during object creation, after setting all properties.
function cmdfile_select_CreateFcn(hObject, eventdata, handles)
% hObject    handle to cmdfile_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes during object deletion, before destroying properties.
function cmdfile_select_DeleteFcn(hObject, eventdata, handles)
% hObject    handle to cmdfile_select (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)











    









%code added by Tao
% --- Executes on button press in pushbutton41.
function pushbutton41_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton41 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%try handle
%datavoltage=handles.datavoltage;
packnumber=handles.packnumber;
%t_capture=now;

i_foldername = get(handles.edit19, 'String');
path = ['experiment', i_foldername];

%cd(path);

%capture=fullfile(path,'myData_capture.dat');

  %global datavoltage
  %global packnumber
saveas(handles.SensorData, [path,'/output_capture',num2str(packnumber)], 'png')

  disp('completed');
  msgbox('capture completed','message')

  %datavoltage=Samples;
  %eval([writematrix,'(Samples',',','myData_',num2str(packetNumber),'.dat',',','Delimiter',',',';)']);

  %eval([writematrix,'(Samples',',','myData_',num2str(packetNumber),'.dat',',','Delimiter',',',';)']);
%   writematrix([packetNumber,1],'myData.dat','Delimiter','tab')  
%   writematrix(Samples(1,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix([packetNumber,3],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix(Samples(3,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append') 
%   writematrix([packetNumber,5],'myData.dat','Delimiter','tab', 'WriteMode' , 'append')
%   writematrix(Samples(5,:),'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  
  %writematrix(packetNumber+1,'myData.dat','Delimiter','tab', 'WriteMode' , 'append')  

%  myData_capture = fullfile(path,' myData_capture.dat');
                 %writematrix(t_capture,myData_capture,'Delimiter','tab', 'WriteMode' , 'append')  
%                 writematrix(datestr(t_capture,'dd-mmm-yyyy HH:MM:SS.FFF'),myData_capture,'Delimiter','tab', 'WriteMode' , 'append')                   
%                 writematrix([packnumber,1], myData_capture,'Delimiter','tab', 'WriteMode' , 'append')  
%                 writematrix(datavoltage(2,:), myData_capture,'Delimiter','tab', 'WriteMode' , 'append')  
%                 writematrix([2], myData_capture,'Delimiter','tab', 'WriteMode' , 'append')  
%                 writematrix(datavoltage(1,:), myData_capture,'Delimiter','tab', 'WriteMode' , 'append') 
%                 writematrix([3], myData_capture,'Delimiter','tab', 'WriteMode' , 'append')
%                 writematrix(datavoltage(3,:), myData_capture,'Delimiter','tab', 'WriteMode' , 'append')  
 
%   writematrix([packnumber,1],'myData_capture.dat','Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix(datavoltage(1,:),'myData_capture.dat','Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix([packnumber,3],'myData_capture.dat','Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix(datavoltage(3,:),'myData_capture.dat','Delimiter','tab', 'WriteMode' , 'append') 
%   writematrix([packnumber,5],'myData_capture.dat','Delimiter','tab', 'WriteMode' , 'append')
%   writematrix(datavoltage(5,:),'myData_capture.dat','Delimiter','tab', 'WriteMode' , 'append')  




%    writematrix([packnumber,1],capture,'Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix(datavoltage(1,:),capture,'Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix([packnumber,3],capture,'Delimiter','tab', 'WriteMode' , 'append')  
%   writematrix(datavoltage(3,:),capture,'Delimiter','tab', 'WriteMode' , 'append') 
%   writematrix([packnumber,5],capture,'Delimiter','tab', 'WriteMode' , 'append')
%   writematrix(datavoltage(5,:),capture,'Delimiter','tab', 'WriteMode' , 'append')  
 
  % type myData.dat

  %save picture with gui interface

  %saveas(gcf, ['output',num2str(packnumber)], 'bmp')
  %saveas(handles.SensorData, ['output_capture',num2str(packnumber)], 'bmp')
  
%cd('..');

    %code added by Tao ended




    %code added by Tao
% --- Executes on button press in togglebutton18.
function togglebutton18_Callback(hObject, eventdata, handles)
% hObject    handle to togglebutton18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of togglebutton18
 button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    % At startup, button_state is set to 'Max'.
%    global reco

    if (button_state == max)
%        record_state=1;
%        handles.record_state=record_state;
%         
%        handles.record_state=1;
% 
%         reco=1;
        set(handles.togglebutton18, 'String', 'Stop Record image');


    elseif (button_state == min)

%        record_state=0;
%        handles.record_state=record_state;
% 
%        %handles.record_state=0;
% 
%         reco=0;
        set(handles.togglebutton18, 'String', 'Start Record image');
   
    

    end


    %code added by Tao ended





     %code added by Tao
% --- Executes on button press in pushbutton42.
function pushbutton42_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton42 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

i_foldername = get(handles.edit19, 'String');
path = ['experiment', i_foldername];

cd(path);

if ~exist('record.txt','file')
    disp('no recent record files')
    msgbox('no recent record files','warning','warn')
else


                   

    v=VideoWriter('guide.avi','Uncompressed AVI');
    v.FrameRate=5;

   
    Read_record=importdata("record.txt");
    Read_record_length=length(Read_record);
    record_start=Read_record(1);
    record_stop=Read_record(Read_record_length);
    
     open (v);
    for i=record_start:record_stop

     if ~exist(['output',num2str(i),'.png'],'file')
         i=i+1;
     else
    
         A=imread(['output',num2str(i)], 'png');
         writeVideo(v,A);
    
         %delete(['output',num2str(i)], 'png');
         delete(['output',num2str(i),'.png']);
     end             
    end
     close(v);
     handles.video=v;
    
    
    delete record.txt;

cd('..');
    disp('Video generated')
    msgbox('Video generated','message')
end



%code added by Tao ended



    


function edit18_Callback(hObject, eventdata, handles)
% hObject    handle to edit18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit18 as text
%        str2double(get(hObject,'String')) returns contents of edit18 as a double


% --- Executes during object creation, after setting all properties.
function edit18_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in popupmenu13.
function popupmenu13_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu13 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu13


% --- Executes during object creation, after setting all properties.
function popupmenu13_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit19_Callback(hObject, eventdata, handles)
% hObject    handle to edit19 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit19 as text
%        str2double(get(hObject,'String')) returns contents of edit19 as a double


% --- Executes during object creation, after setting all properties.
function edit19_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit19 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton43.
function pushbutton43_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton43 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



function edit17_Callback(hObject, eventdata, handles)
% hObject    handle to edit17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit17 as text
%        str2double(get(hObject,'String')) returns contents of edit17 as a double


% --- Executes during object creation, after setting all properties.
function edit17_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in popupmenu12.
function popupmenu12_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu12 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu12


% --- Executes during object creation, after setting all properties.
function popupmenu12_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit20_Callback(hObject, eventdata, handles)
% hObject    handle to edit20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit20 as text
%        str2double(get(hObject,'String')) returns contents of edit20 as a double


% --- Executes during object creation, after setting all properties.
function edit20_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit21_Callback(hObject, eventdata, handles)
% hObject    handle to edit21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit21 as text
%        str2double(get(hObject,'String')) returns contents of edit21 as a double


% --- Executes during object creation, after setting all properties.
function edit21_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton45.



function edit24_Callback(hObject, eventdata, handles)
% hObject    handle to edit24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit24 as text
%        str2double(get(hObject,'String')) returns contents of edit24 as a double


% --- Executes during object creation, after setting all properties.
function edit24_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton46.
function pushbutton46_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton46 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%code added by Tao
    i_foldername = get(handles.edit19, 'String');
    path = ['experiment', i_foldername];


    %record experiment settings information
    notes_content = get (handles.edit24, 'string');


    if ~exist(path,'dir')
        disp('Please first choose a valid data folder')
        msgbox('Please first choose a valid data folder','warning','error')
    else
            settingfilename = fullfile(path,'Notes.txt');
            f=fopen(settingfilename,'a');

            tNow = now;
            fprintf(f,'Time: %s \r\n',datestr(tNow,'dd-mmm-yyyy HH:MM:SS.FFF'));

            fprintf(f,'Notes: %s \r\n',notes_content);
            fclose(f);
            disp('Notes saved.')
            msgbox('Notes saved','message')
   
    end
    
    %code added by Tao ended


     %code added by Tao


% --- Executes on button press in radiobutton10.
function radiobutton10_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton10

    %code added by Tao ended



function edit26_Callback(hObject, eventdata, handles)
% hObject    handle to edit26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit26 as text
%        str2double(get(hObject,'String')) returns contents of edit26 as a double


% --- Executes during object creation, after setting all properties.
function edit26_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit27_Callback(hObject, eventdata, handles)
% hObject    handle to edit27 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit27 as text
%        str2double(get(hObject,'String')) returns contents of edit27 as a double





% --- Executes during object creation, after setting all properties.
function edit27_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit27 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in lock_trace_mark.
function lock_trace_mark_Callback(hObject, eventdata, handles)
% hObject    handle to lock_trace_mark (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    % At startup, button_state is set to 'Max'.

    if (button_state == max)
        judge=0;

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
        
        if isempty(get(handles.edit1m1,'string'))==0 %judgement on if marks number is valid
            if isempty(st1m1) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit1m1, 'String', '');
            else
                if rem(st1m1,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit1m1, 'String', '');
                else
                    if st1m1 <=0 || st1m1>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit1m1, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024
         
        if isempty(get(handles.edit1m2,'string'))==0 %judgement on if marks number is valid
            if isempty(st1m2) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit1m2, 'String', '');
            else
                if rem(st1m2,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit1m2, 'String', '');
                else
                    if st1m2 <=0 || st1m2>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit1m2, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit1m3,'string'))==0 %judgement on if marks number is valid
            if isempty(st1m3) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit1m3, 'String', '');
            else
                if rem(st1m3,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit1m3, 'String', '');
                else
                    if st1m3 <=0 || st1m3>=1024  
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit1m3, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit1m4,'string'))==0 %judgement on if marks number is valid
            if isempty(st1m4) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit1m4, 'String', '');
            else
                if rem(st1m4,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit1m4, 'String', '');
                else
                    if st1m4 <=0 || st1m4>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit1m4, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit1m5,'string'))==0 %judgement on if marks number is valid
            if isempty(st1m5) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit1m5, 'String', '');
            else
                if rem(st1m5,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit1m5, 'String', '');
                else
                    if st1m5 <=0 || st1m5>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit1m5, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024


        if isempty(get(handles.edit2m1,'string'))==0 %judgement on if marks number is valid
            if isempty(st2m1) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit2m1, 'String', '');
            else
                if rem(st2m1,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit2m1, 'String', '');
                else
                    if st2m1 <=0 || st2m1>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit2m1, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024
         
        if isempty(get(handles.edit2m2,'string'))==0 %judgement on if marks number is valid
            if isempty(st2m2) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit2m2, 'String', '');
            else
                if rem(st2m2,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit2m2, 'String', '');
                else
                    if st2m2 <=0 || st2m2>=1024  
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit2m2, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit2m3,'string'))==0 %judgement on if marks number is valid
            if isempty(st2m3) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit2m3, 'String', '');
            else
                if rem(st2m3,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit2m3, 'String', '');
                else
                    if st2m3 <=0 || st2m3>=1024  
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit2m3, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit2m4,'string'))==0 %judgement on if marks number is valid
            if isempty(st2m4) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit2m4, 'String', '');
            else
                if rem(st2m4,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit2m4, 'String', '');
                else
                    if st2m4 <=0 || st2m4>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit2m4, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit2m5,'string'))==0 %judgement on if marks number is valid
            if isempty(st2m5) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit2m5, 'String', '');
            else
                if rem(st2m5,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit2m5, 'String', '');
                else
                    if st2m5 <=0 || st2m5>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit2m5, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit3m1,'string'))==0 %judgement on if marks number is valid
            if isempty(st3m1) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit3m1, 'String', '');
            else
                if rem(st3m1,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit3m1, 'String', '');
                else
                    if st3m1 <=0 || st3m1>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit3m1, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024
         
        if isempty(get(handles.edit3m2,'string'))==0 %judgement on if marks number is valid
            if isempty(st3m2) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit3m2, 'String', '');
            else
                if rem(st3m2,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit3m2, 'String', '');
                else
                    if st3m2 <=0 || st3m2>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit3m2, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit3m3,'string'))==0 %judgement on if marks number is valid
            if isempty(st3m3) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit3m3, 'String', '');
            else
                if rem(st3m3,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit3m3, 'String', '');
                else
                    if st3m3 <=0 || st3m3>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit3m3, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit3m4,'string'))==0 %judgement on if marks number is valid
            if isempty(st3m4) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit3m4, 'String', '');
            else
                if rem(st3m4,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit3m4, 'String', '');
                else
                    if st3m4 <=0 || st3m4>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit3m4, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024

        if isempty(get(handles.edit3m5,'string'))==0 %judgement on if marks number is valid
            if isempty(st3m5) == 1
                 msgbox('Please enter number','warning','error')
                 set(handles.edit3m5, 'String', '');
            else
                if rem(st3m5,1) ~=0
                    msgbox('Please enter int number','warning','error')
                    set(handles.edit3m5, 'String', '');
                else
                    if st3m5 <=0 || st3m5>=1024   
                        msgbox('Please enter number between 1-1023','warning','error')
                        set(handles.edit3m5, 'String', '');
                    else
                        judge=judge+1;
                    end
                end
            end
        else
            judge=judge+1;
        end                 %mark should be empty or int number between 1-1024



         if judge==15
           
            set(handles.edit1m1, 'Enable', 'off'); % Disable the editable text, so user can't change the edit
            set(handles.edit1m2, 'Enable', 'off');
            set(handles.edit1m3, 'Enable', 'off');
            set(handles.edit1m4, 'Enable', 'off');
            set(handles.edit1m5, 'Enable', 'off');
            set(handles.edit2m1, 'Enable', 'off'); 
            set(handles.edit2m2, 'Enable', 'off');
            set(handles.edit2m3, 'Enable', 'off');
            set(handles.edit2m4, 'Enable', 'off');
            set(handles.edit2m5, 'Enable', 'off');
            set(handles.edit3m1, 'Enable', 'off'); 
            set(handles.edit3m2, 'Enable', 'off');
            set(handles.edit3m3, 'Enable', 'off');
            set(handles.edit3m4, 'Enable', 'off');
            set(handles.edit3m5, 'Enable', 'off');

            set(handles.edit1m1, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit1m2, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit1m3, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit1m4, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit1m5, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit2m1, 'BackgroundColor', [0.94 0.94 0.94]); 
            set(handles.edit2m2, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit2m3, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit2m4, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit2m5, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit3m1, 'BackgroundColor', [0.94 0.94 0.94]); 
            set(handles.edit3m2, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit3m3, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit3m4, 'BackgroundColor', [0.94 0.94 0.94]);
            set(handles.edit3m5, 'BackgroundColor', [0.94 0.94 0.94]);

        set(handles.lock_trace_mark, 'String', 'Unlock');

        guidata(hObject,handles);
        handles.stlockstatus=1;
        guidata(hObject,handles);

     %{
        NumberOfSensingFields = size(handles.SensingFields.Name,1);
        W = cell(NumberOfSensingFields,3); %preallocate empty cell array
            for nA = 1:NumberOfSensingFields

            end
     %}

        
        if isempty(st1m1)==0
            if isempty(st1m2)==1
                legend(handles.SubPlots(7),['P',num2str(st1m1)])
            else
                if isempty(st1m3)==1
                    legend(handles.SubPlots(7),['P',num2str(st1m1)],['P',num2str(st1m2)])
                else
                    if isempty(st1m4)==1;
                        legend(handles.SubPlots(7),['P',num2str(st1m1)],['P',num2str(st1m2)],['P',num2str(st1m3)])
                    else
                        if isempty(st1m5)==1;
                            legend(handles.SubPlots(7),['P',num2str(st1m1)],['P',num2str(st1m2)],['P',num2str(st1m3)],['P',num2str(st1m4)])
                        else
                            legend(handles.SubPlots(7),['P',num2str(st1m1)],['P',num2str(st1m2)],['P',num2str(st1m3)],['P',num2str(st1m4)],['P',num2str(st1m5)])
                        end
                    end
                end
            end
        end

    if isempty(st2m1)==0
            if isempty(st2m2)==1
                legend(handles.SubPlots(8),['P',num2str(st2m1)])


                %line([1.089,1.089+5.32],[1.089,1.089],'color','r','linewidth',2);
            else
                if isempty(st2m3)==1
                    legend(handles.SubPlots(8),['P',num2str(st2m1)],['P',num2str(st2m2)])
                else
                    if isempty(st2m4)==1;
                        legend(handles.SubPlots(8),['P',num2str(st2m1)],['P',num2str(st2m2)],['P',num2str(st2m3)])
                    else
                        if isempty(st2m5)==1;
                            legend(handles.SubPlots(8),['P',num2str(st2m1)],['P',num2str(st2m2)],['P',num2str(st2m3)],['P',num2str(st2m4)])
                        else
                            legend(handles.SubPlots(8),['P',num2str(st2m1)],['P',num2str(st2m2)],['P',num2str(st2m3)],['P',num2str(st2m4)],['P',num2str(st2m5)])
                        end
                    end
                end
            end
        end

       if isempty(st3m1)==0
            if isempty(st3m2)==1
                legend(handles.SubPlots(9),['P',num2str(st3m1)])
            else
                if isempty(st3m3)==1
                    legend(handles.SubPlots(9),['P',num2str(st3m1)],['P',num2str(st3m2)])
                else
                    if isempty(st3m4)==1;
                        legend(handles.SubPlots(9),['P',num2str(st3m1)],['P',num2str(st3m2)],['P',num2str(st3m3)])
                    else
                        if isempty(st3m5)==1;
                            legend(handles.SubPlots(9),['P',num2str(st3m1)],['P',num2str(st3m2)],['P',num2str(st3m3)],['P',num2str(st3m4)])
                        else
                            legend(handles.SubPlots(9),['P',num2str(st3m1)],['P',num2str(st3m2)],['P',num2str(st3m3)],['P',num2str(st3m4)],['P',num2str(st3m5)])
                        end
                    end
                end
            end
        end

         

        end

    elseif (button_state == min)

            set(handles.edit1m1, 'Enable', 'on'); % enable the editable text, so user can change the edit
            set(handles.edit1m2, 'Enable', 'on');
            set(handles.edit1m3, 'Enable', 'on');
            set(handles.edit1m4, 'Enable', 'on');
            set(handles.edit1m5, 'Enable', 'on');
            set(handles.edit2m1, 'Enable', 'on'); 
            set(handles.edit2m2, 'Enable', 'on');
            set(handles.edit2m3, 'Enable', 'on');
            set(handles.edit2m4, 'Enable', 'on');
            set(handles.edit2m5, 'Enable', 'on');
            set(handles.edit3m1, 'Enable', 'on'); 
            set(handles.edit3m2, 'Enable', 'on');
            set(handles.edit3m3, 'Enable', 'on');
            set(handles.edit3m4, 'Enable', 'on');
            set(handles.edit3m5, 'Enable', 'on');

            set(handles.edit1m1, 'BackgroundColor', 'w');
            set(handles.edit1m2, 'BackgroundColor', 'w');
            set(handles.edit1m3, 'BackgroundColor', 'w');
            set(handles.edit1m4, 'BackgroundColor', 'w');
            set(handles.edit1m5, 'BackgroundColor', 'w');
            set(handles.edit2m1, 'BackgroundColor', 'w'); 
            set(handles.edit2m2, 'BackgroundColor', 'w');
            set(handles.edit2m3, 'BackgroundColor', 'w');
            set(handles.edit2m4, 'BackgroundColor', 'w');
            set(handles.edit2m5, 'BackgroundColor', 'w');
            set(handles.edit3m1, 'BackgroundColor', 'w'); 
            set(handles.edit3m2, 'BackgroundColor', 'w');
            set(handles.edit3m3, 'BackgroundColor', 'w');
            set(handles.edit3m4, 'BackgroundColor', 'w');
            set(handles.edit3m5, 'BackgroundColor', 'w');


            set(handles.lock_trace_mark, 'String', 'lock');
            
            legend(handles.SubPlots(7),"off");
            legend(handles.SubPlots(8),"off");
            legend(handles.SubPlots(9),"off");

            guidata(hObject,handles);
            handles.stlockstatus=0;
            guidata(hObject,handles);



    end




function edit1m1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1m1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1m1 as text
%        str2double(get(hObject,'String')) returns contents of edit1m1 as a double


% --- Executes during object creation, after setting all properties.
function edit1m1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1m1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2m1_Callback(hObject, eventdata, handles)
% hObject    handle to edit2m1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2m1 as text
%        str2double(get(hObject,'String')) returns contents of edit2m1 as a double


% --- Executes during object creation, after setting all properties.
function edit2m1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2m1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton51.
function pushbutton51_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton51 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    guidata(hObject, handles);
     handles.x1=0; %re-set handles for signal trace initial value
     handles.x2=0;
     handles.x3=0;
     handles.X1=[];
     handles.X2=[];
     handles.X3=[];
     handles.Y11=[];
     handles.Y12=[];
     handles.Y13=[];
     handles.Y14=[];
     handles.Y15=[];
     handles.Y21=[];
     handles.Y22=[];
     handles.Y23=[];
     handles.Y24=[];
     handles.Y25=[];
     handles.Y31=[];
     handles.Y32=[];
     handles.Y33=[];
     handles.Y34=[];
     handles.Y35=[];

     guidata(hObject,handles);





function edit3m1_Callback(hObject, eventdata, handles)
% hObject    handle to edit3m1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3m1 as text
%        str2double(get(hObject,'String')) returns contents of edit3m1 as a double


% --- Executes during object creation, after setting all properties.
function edit3m1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3m1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit1m2_Callback(hObject, eventdata, handles)
% hObject    handle to edit1m2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1m2 as text
%        str2double(get(hObject,'String')) returns contents of edit1m2 as a double


% --- Executes during object creation, after setting all properties.
function edit1m2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1m2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2m2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2m2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2m2 as text
%        str2double(get(hObject,'String')) returns contents of edit2m2 as a double


% --- Executes during object creation, after setting all properties.
function edit2m2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2m2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit3m2_Callback(hObject, eventdata, handles)
% hObject    handle to edit3m2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3m2 as text
%        str2double(get(hObject,'String')) returns contents of edit3m2 as a double


% --- Executes during object creation, after setting all properties.
function edit3m2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3m2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit1m3_Callback(hObject, eventdata, handles)
% hObject    handle to edit1m3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1m3 as text
%        str2double(get(hObject,'String')) returns contents of edit1m3 as a double


% --- Executes during object creation, after setting all properties.
function edit1m3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1m3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2m3_Callback(hObject, eventdata, handles)
% hObject    handle to edit2m3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2m3 as text
%        str2double(get(hObject,'String')) returns contents of edit2m3 as a double


% --- Executes during object creation, after setting all properties.
function edit2m3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2m3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit3m3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3m3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3m3 as text
%        str2double(get(hObject,'String')) returns contents of edit3m3 as a double


% --- Executes during object creation, after setting all properties.
function edit3m3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3m3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit1m4_Callback(hObject, eventdata, handles)
% hObject    handle to edit1m4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1m4 as text
%        str2double(get(hObject,'String')) returns contents of edit1m4 as a double


% --- Executes during object creation, after setting all properties.
function edit1m4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1m4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2m4_Callback(hObject, eventdata, handles)
% hObject    handle to edit2m4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2m4 as text
%        str2double(get(hObject,'String')) returns contents of edit2m4 as a double


% --- Executes during object creation, after setting all properties.
function edit2m4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2m4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit3m4_Callback(hObject, eventdata, handles)
% hObject    handle to edit3m4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3m4 as text
%        str2double(get(hObject,'String')) returns contents of edit3m4 as a double


% --- Executes during object creation, after setting all properties.
function edit3m4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3m4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit1m5_Callback(hObject, eventdata, handles)
% hObject    handle to edit1m5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1m5 as text
%        str2double(get(hObject,'String')) returns contents of edit1m5 as a double


% --- Executes during object creation, after setting all properties.
function edit1m5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1m5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2m5_Callback(hObject, eventdata, handles)
% hObject    handle to edit2m5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2m5 as text
%        str2double(get(hObject,'String')) returns contents of edit2m5 as a double


% --- Executes during object creation, after setting all properties.
function edit2m5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2m5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit3m5_Callback(hObject, eventdata, handles)
% hObject    handle to edit3m5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3m5 as text
%        str2double(get(hObject,'String')) returns contents of edit3m5 as a double


% --- Executes during object creation, after setting all properties.
function edit3m5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3m5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end






function edit28_Callback(hObject, eventdata, handles)
% hObject    handle to edit28 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit28 as text
%        str2double(get(hObject,'String')) returns contents of edit28 as a double


% --- Executes during object creation, after setting all properties.
function edit28_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit28 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit29_Callback(hObject, eventdata, handles)
% hObject    handle to edit29 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit29 as text
%        str2double(get(hObject,'String')) returns contents of edit29 as a double


% --- Executes during object creation, after setting all properties.
function edit29_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit29 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit30_Callback(hObject, eventdata, handles)
% hObject    handle to edit30 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit30 as text
%        str2double(get(hObject,'String')) returns contents of edit30 as a double


% --- Executes during object creation, after setting all properties.
function edit30_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit30 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton49.
function pushbutton49_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton49 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton48.
function pushbutton48_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton48 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --- Executes on button press in radiobutton11.
function radiobutton11_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton11


% --- Executes on button press in pushbutton45.
function pushbutton45_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton45 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    %code added by Tao
    i_foldername = get(handles.edit19, 'String');
        
        %create new folder;
    
        if exist(['experiment', i_foldername]','dir')==0
            mkdir (['experiment', i_foldername])
            disp('Folder created.')
            msgbox('Folder created','message')
        else
            disp('Warning: Folder already exists.')
            msgbox('Folder already exists, data will be saved in this folder','warning','warn')
        end
    


        %code added by Tao
        %pre-allocate for video record
                %handles.record_state=0;       %presetting of start_record button state
                

        %code added by Tao ended
    
    %code added by Tao ended


% --- Executes on button press in pushbutton44.
function pushbutton44_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%code added by Tao
    i_foldername = get(handles.edit19, 'String');
    path = ['experiment', i_foldername];


    %record experiment settings information
    temp_value = get (handles.edit20, 'string');
    pressure_value = get (handles.edit21, 'string');


    a=isempty(temp_value)||isempty(pressure_value);


    if ~exist(path,'dir')
        disp('Please first choose a valid data folder')
        msgbox('Please first choose a valid data folder','warning','error')
    else

        if a==1
            disp('Information incomplete.')
            msgbox('Information incomplete','warning','warn')
            
        else
            %settingfilename = fullfile(['experiment', i_foldername],['setting_information', i_foldername,'.txt'])
            settingfilename = fullfile(path,'setting_information.txt');
            f=fopen(settingfilename,'w');

            tNow = now;
            fprintf(f,'Time: %s \r\n',datestr(tNow,'dd-mmm-yyyy HH:MM:SS.FFF'));

            fprintf(f,'Temperature: %s ℃\r\n',temp_value);
            fprintf(f,'Pressure: %s Pa\r\n',pressure_value);
    
            fclose(f);
            disp('ready to start.')
            msgbox('ready to start','message','help')
    
                        %save(settingfilename,'temp_value','-append')
             %fprintf(settingfilename,'Temperature: %d oC',temp_value);
        end
    end
    
    %code added by Tao ended



function edit47_Callback(hObject, eventdata, handles)
% hObject    handle to edit47 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit47 as text
%        str2double(get(hObject,'String')) returns contents of edit47 as a double


% --- Executes during object creation, after setting all properties.
function edit47_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit47 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in radiobutton12.
function radiobutton12_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton12


% --- Executes on button press in radiobutton13.
function radiobutton13_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton13


% --- Executes on button press in togglebutton20.
function togglebutton20_Callback(hObject, eventdata, handles)
% hObject    handle to togglebutton20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of togglebutton20
 button_state = get(hObject, 'Value');
    max = get(hObject, 'Max');
    min = get(hObject, 'Min');
    % At startup, button_state is set to 'Max'.


   lock = get(handles.lock_trace_mark, 'Value');
    max_lock = get(handles.lock_trace_mark, 'Max');
    min_lock = get(handles.lock_trace_mark, 'Min');

    if (button_state == max)

        if (lock == min_lock)
            msgbox('Please first lock the signal trace mark','warning','error')
        end

        if (lock == max_lock)

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
        
        set(handles.togglebutton20, 'String', 'Hide position');

         if isempty(st1m1)==0
            a = handles.SensingFields.a(1);
            b = handles.SensingFields.b(1);
            a1 = handles.SensingFields.a1(1);
            b1 = handles.SensingFields.b1(1);

            
            order=mod(st1m1,32);
            if order ==0
                line=floor(st1m1/32);
                order=32;
            else
                line=floor(st1m1/32)+1;
            end
            oddoreven=mod(line,2);
            
            if (oddoreven == 1)

                    set(handles.markimage1(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage2(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage3(1),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage4(1),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage1(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage2(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage3(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage4(1),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


         if isempty(st1m2)==0
            a = handles.SensingFields.a(1);
            b = handles.SensingFields.b(1);
            a1 = handles.SensingFields.a1(1);
            b1 = handles.SensingFields.b1(1);

            order=mod(st1m2,32);
            if order ==0
                line=floor(st1m2/32);
                order=32;
            else
                line=floor(st1m2/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage5(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage6(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage7(1),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage8(1),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage5(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage6(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage7(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage8(1),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


         if isempty(st1m3)==0
            a = handles.SensingFields.a(1);
            b = handles.SensingFields.b(1);
            a1 = handles.SensingFields.a1(1);
            b1 = handles.SensingFields.b1(1);

            order=mod(st1m3,32);
            if order ==0
                line=floor(st1m3/32);
                order=32;
            else
                line=floor(st1m3/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage9(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage10(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage11(1),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage12(1),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage9(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage10(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage11(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage12(1),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


        if isempty(st1m4)==0
            a = handles.SensingFields.a(1);
            b = handles.SensingFields.b(1);
            a1 = handles.SensingFields.a1(1);
            b1 = handles.SensingFields.b1(1);

            order=mod(st1m4,32);
            if order ==0
                line=floor(st1m4/32);
                order=32;
            else
                line=floor(st1m4/32)+1;
            end
            oddoreven=mod(line,2);
             if (oddoreven == 1)

                    set(handles.markimage13(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage14(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage15(1),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage16(1),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage13(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage14(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage15(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage16(1),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end

        if isempty(st1m5)==0
            a = handles.SensingFields.a(1);
            b = handles.SensingFields.b(1);
            a1 = handles.SensingFields.a1(1);
            b1 = handles.SensingFields.b1(1);

            order=mod(st1m5,32);
            if order ==0
                line=floor(st1m5/32);
                order=32;
            else
                line=floor(st1m5/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage17(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage18(1),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage19(1),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage20(1),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage17(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage18(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage19(1),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage20(1),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end







        if isempty(st2m1)==0
            a = handles.SensingFields.a(2);
            b = handles.SensingFields.b(2);
            a1 = handles.SensingFields.a1(2);
            b1 = handles.SensingFields.b1(2);

            order=mod(st2m1,32);
            if order ==0
                line=floor(st2m1/32);
                order=32;
            else
                line=floor(st2m1/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage1(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage2(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage3(2),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage4(2),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage1(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage2(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage3(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage4(2),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


         if isempty(st2m2)==0
            a = handles.SensingFields.a(2);
            b = handles.SensingFields.b(2);
            a1 = handles.SensingFields.a1(2);
            b1 = handles.SensingFields.b1(2);


            order=mod(st2m2,32);
            if order ==0
                line=floor(st2m2/32);
                order=32;
            else
                line=floor(st2m2/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage5(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage6(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage7(2),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage8(2),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage5(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage6(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage7(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage8(2),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


         if isempty(st2m3)==0
            a = handles.SensingFields.a(2);
            b = handles.SensingFields.b(2);
            a1 = handles.SensingFields.a1(2);
            b1 = handles.SensingFields.b1(2);

            order=mod(st2m3,32);
            if order ==0
                line=floor(st2m3/32);
                order=32;
            else
                line=floor(st2m3/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage9(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage10(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage11(2),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage12(2),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage9(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage10(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage11(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage12(2),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


        if isempty(st2m4)==0
            a = handles.SensingFields.a(2);
            b = handles.SensingFields.b(2);
            a1 = handles.SensingFields.a1(2);
            b1 = handles.SensingFields.b1(2);

                        order=mod(st2m4,32);
            if order ==0
                line=floor(st2m4/32);
                order=32;
            else
                line=floor(st2m4/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage13(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage14(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage15(2),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage16(2),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage13(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage14(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage15(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage16(2),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end

        if isempty(st2m5)==0
            a = handles.SensingFields.a(2);
            b = handles.SensingFields.b(2);
            a1 = handles.SensingFields.a1(2);
            b1 = handles.SensingFields.b1(2);

                        order=mod(st2m5,32);
            if order ==0
                line=floor(st2m5/32);
                order=32;
            else
                line=floor(st2m5/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage17(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage18(2),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage19(2),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage20(2),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage17(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage18(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage19(2),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage20(2),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end



        if isempty(st3m1)==0
            a = handles.SensingFields.a(3);
            b = handles.SensingFields.b(3);
            a1 = handles.SensingFields.a1(3);
            b1 = handles.SensingFields.b1(3);

            
            order=mod(st3m1,32);
            if order ==0
                line=floor(st3m1/32);
                order=32;
            else
                line=floor(st3m1/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage1(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage2(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage3(3),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage4(3),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage1(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage2(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage3(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage4(3),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


         if isempty(st3m2)==0
            a = handles.SensingFields.a(3);
            b = handles.SensingFields.b(3);
            a1 = handles.SensingFields.a1(3);
            b1 = handles.SensingFields.b1(3);


            order=mod(st3m2,32);
            if order ==0
                line=floor(st3m2/32);
                order=32;
            else
                line=floor(st3m2/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage5(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage6(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage7(3),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage8(3),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage5(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage6(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage7(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage8(3),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


         if isempty(st3m3)==0
            a = handles.SensingFields.a(3);
            b = handles.SensingFields.b(3);
            a1 = handles.SensingFields.a1(3);
            b1 = handles.SensingFields.b1(3);


            order=mod(st3m3,32);
            if order ==0
                line=floor(st3m3/32);
                order=32;
            else
                line=floor(st3m3/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage9(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage10(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage11(3),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage12(3),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage9(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage10(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage11(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage12(3),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end


        if isempty(st3m4)==0
            a = handles.SensingFields.a(3);
            b = handles.SensingFields.b(3);
            a1 = handles.SensingFields.a1(3);
            b1 = handles.SensingFields.b1(3);

            order=mod(st3m4,32);
            if order ==0
                line=floor(st3m4/32);
                order=32;
            else
                line=floor(st3m4/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage13(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage14(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage15(3),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage16(3),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage13(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage14(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage15(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
                    set(handles.markimage16(3),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end

        if isempty(st3m5)==0
            a = handles.SensingFields.a(3);
            b = handles.SensingFields.b(3);
            a1 = handles.SensingFields.a1(3);
            b1 = handles.SensingFields.b1(3);


            order=mod(st3m5,32);
            if order ==0
                line=floor(st3m5/32);
                order=32;
            else
                line=floor(st3m5/32)+1;
            end
            oddoreven=mod(line,2);
            if (oddoreven == 1)

                    set(handles.markimage17(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(33-order)*a]);
                    set(handles.markimage18(3),'XData',[(floor(line/2))*b,(floor(line/2)+1)*b],'YData',[(34-order)*a,(34-order)*a]);
                    set(handles.markimage19(3),'XData',[(floor(line/2))*b,(floor(line/2))*b],'YData',[(33-order)*a,(34-order)*a]);
                    set(handles.markimage20(3),'XData',[(floor(line/2)+1)*b,(floor(line/2)+1)*b],'YData',[(33-order)*a,(34-order)*a]);
            else
                    set(handles.markimage17(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,order*a-a1]);
                    set(handles.markimage18(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2))*b+b1],'YData',[(order+1)*a-a1,(order+1)*a-a1]);
                    set(handles.markimage19(3),'XData',[(floor(line/2)-1)*b+b1,(floor(line/2)-1)*b+b1],'YData',[order*a-a1,(order+1)*a]-a1);
                    set(handles.markimage20(3),'XData',[(floor(line/2))*b+b1,(floor(line/2))*b+b1],'YData',[order*a-a1,(order+1)*a-a1]);
            end
         end

        











       end  
    end
    if (button_state == min)
        for i=1:3
        set(handles.markimage1(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage2(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage3(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage4(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage5(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage6(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage7(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage8(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage9(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage10(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage11(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage12(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage13(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage14(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage15(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage16(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage17(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage18(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage19(i),'XData',[-1,-1],'YData',[-2,-1]);
        set(handles.markimage20(i),'XData',[-1,-1],'YData',[-2,-1]);
        end
    
    set(handles.togglebutton20, 'String', 'Show position');
    end






% --- Executes on button press in radiobutton14.
function radiobutton14_Callback(hObject, eventdata, handles)

cmd = 'cap 999';
com_sendcmd(handles, cmd);



% hObject    handle to radiobutton14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton14


% --- Executes on button press in storedata.
function storedata_Callback(hObject, eventdata, handles)
% hObject    handle to storedata (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%extract data from Data_Raw_tst.dat
dataread=fopen('C:\LocalData\css_Data\CSSa_Raw_tst.dat');
%a=fgets(dataread);
d=[];
i=1;
while i<2   
    packetNumberBytes = fread(dataread,4,'uint8');
    if isempty(packetNumberBytes)==1
        i=2;
    else
        packetNumber = [1677216,65536,256,1] * packetNumberBytes;
        packetDataBytes = fread(dataread,[12,1024],'uint8');
        packetDataMasks = [16,32,64];
        Samples = zeros(3,1024);
        for n = 1:3
            Samples(n,:) = [2048,1024,512,256,128,64,32,16,8,4,2,1] * bitshift(bitand(packetDataBytes,packetDataMasks(n)),-3-n); %decode smaples from packet data bytes
            Samples(n,1024) = 0; %invalid sample in case of Single Cell scan mode --> Make consistent with user-selected scan mode
        end
        d1=[packetNumber;1;Samples(2,:)';2;Samples(1,:)';3;Samples(3,:)'];
        d=[d,d1];
    end
end
fclose(dataread);



%saveas another file (in the format compatible for the readout app) in the
%path user assigned in guide app.
a=max(d,[],2); %find the max packetnumber (as there would be several error packet in the beginning)
l=width(d); %total packet number in raw file (incl. error packet)
d_final=d(:,l-a(1)+1:l);

i_foldername = get(handles.edit19, 'String');
path = ['experiment', i_foldername];

myData= fullfile(path,'myData.dat');
writematrix(d_final, myData);

 disp('completed');
 msgbox('data saved','message')
