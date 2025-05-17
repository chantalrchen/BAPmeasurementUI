function [W0,W1,W2] = WeightsLinear(M, N, M1, N1)
M2 = M-M1;
N2 = N-N1;

%Points:
R0 = [M; N2]; %target point
R1 = [0; N2]; %left-middle neighbor point
R2 = [M1; 0]; %left-top neighbor point
R3 = [M1+M; 0]; %right-top neighbor point
R4 = [2*M; N2]; %right-middle neighbor point
R5 = [M1+M; N]; %right-bottom neighbor point
R6 = [M1; N]; %left-bottom neighbor point

%Preallocation and initialization:
W0 = zeros(2*M,N); %linear interpolation weigths of target point
W1 = zeros(2*M,N); %linear interpolation weigths of 1st neighbor point
W2 = zeros(2*M,N); %linear interpolation weigths of 2nd neighbor point

%In the following points on tilted edges of triangles are detected with
%integer arithmetic to avoid missing them because of rounding errors in
%floating point arithmetic

%Left-top rectangle:
A = [R1-R0,R2-R0]^(-1); %R1/R2 are 1st/2nd neighbor points
for i=1:M
   for j=1:N2
       if (2*i-1)*N2-(2*(N2-j+1)-1)*M1==0 %detect points on left edge (= outer edge)
           V2 = (i-0.5)/M1;
           %W0(i,j) remains 0
           W1(i,j) = 0.5*(1-V2); %half weight on outer edge
           W2(i,j) = 0.5*V2; %half weight on outer edge
       elseif ~((2*(M-i+1)-1)*N2-(2*(N2-j+1)-1)*M2==0) %detect remaining points not on right edge (= inner edge)
           V = A*([i-0.5;j-0.5]-R0); %all components of V are <1 because search domain is minimal rectangular enclosure of triangle
           if V(1)>0 && 1-V(1)-V(2)>0 %detect remaining points inside triangle(V(2)>0 in current search region)
               W0(i,j) = 1-V(1)-V(2);
               W1(i,j) = V(1);
               W2(i,j) = V(2);
           end
       end
   end
end

%Center-top rectangle:
A = [R3-R0,R2-R0]^(-1); %R3/R2 are 1st/2nd neighbor points
for i=M1+1:M1+M
   for j=1:N2
       if (2*(M-i+1)-1)*N2-(2*(N2-j+1)-1)*M2==0 %detect points on left edge (= inner edge)
           V2 = (M-i+1-0.5)/M2;
           W0(i,j) = 1-V2;
           %W1(i,j) remains 0
           W2(i,j) = V2;
       elseif (2*(i-M)-1)*N2-(2*(N2-j+1)-1)*M1==0 %detect remaining points on right edge (= inner edge)
           V1 = (i-M-0.5)/M1;
           W0(i,j) = 1-V1;
           W1(i,j) = V1;
           %W2(i,j) remains 0
       else
           V = A*([i-0.5;j-0.5]-R0); %all components of V are <1 because search domain is minimal rectangular enclosure of triangle
           if V(1)>0 && V(2)>0 %detect remaining points inside triangle (1-V(1)-V(2)>0 in current search region)
               W0(i,j) = 1-V(1)-V(2);
               W1(i,j) = V(1);
               W2(i,j) = V(2);
           end
       end
   end
end

%Right-top rectangle:
A = [R3-R0,R4-R0]^(-1); %R3/R4 are 1st/2nd neighbor points
for i=M+1:2*M
   for j=1:N2
       if (2*(2*M-i+1)-1)*N2-(2*(N2-j+1)-1)*M2==0 %detect points on right edge (= outer edge)
           V1 = (2*M-i+1-0.5)/M2;
           %W0(i,j) remains 0
           W1(i,j) = 0.5*V1; %half weight on outer edge
           W2(i,j) = 0.5*(1-V1); %half weight on outer edge
       elseif ~((2*(i-M)-1)*N2-(2*(N2-j+1)-1)*M1==0) %detect remaining points not on left edge (= inner edge)
           V = A*([i-0.5;j-0.5]-R0); %all components of V are <1 because search domain is minimal rectangular enclosure of triangle
           if V(2)>0 && 1-V(1)-V(2)>0 %detect remaining points inside triangle(V(1)>0 in current search region)
               W0(i,j) = 1-V(1)-V(2);
               W1(i,j) = V(1);
               W2(i,j) = V(2);
           end
       end
   end
end

%Right-bottom rectangle:
A = [R5-R0,R4-R0]^(-1); %R5/R4 are 1st/2nd neighbor points
for i=M+1:2*M
   for j=N2+1:N
       if (2*(2*M-i+1)-1)*N1-(2*(j-N2)-1)*M2==0 %detect points on right edge (= outer edge)
           V1 = (2*M-i+1-0.5)/M2;
           %W0(i,j) remains 0
           W1(i,j) = 0.5*V1; %half weight on outer edge
           W2(i,j) = 0.5*(1-V1); %half weight on outer edge
       elseif ~((2*(i-M)-1)*N1-(2*(j-N2)-1)*M1==0) %detect remaining points not on left edge (= inner edge)
           V = A*([i-0.5;j-0.5]-R0); %all components of V are <1 because search domain is minimal rectangular enclosure of triangle
           if V(2)>0 && 1-V(1)-V(2)>0 %detect remaining points inside triangle(V(1)>0 in current search region)
               W0(i,j) = 1-V(1)-V(2);
               W1(i,j) = V(1);
               W2(i,j) = V(2);
           end
       end
   end
end

%Center-bottom rectangle:
A = [R5-R0,R6-R0]^(-1); %R5/R6 are 1st/2nd neighbor points
for i=M1+1:M1+M
   for j=N2+1:N
       if (2*(M-i+1)-1)*N1-(2*(j-N2)-1)*M2==0 %detect points on left edge (= inner edge)
           V2 = (M-i+1-0.5)/M2;
           W0(i,j) = 1-V2;
           %W1(i,j) remains 0
           W2(i,j) = V2;
       elseif (2*(i-M)-1)*N1-(2*(j-N2)-1)*M1==0 %detect remaining points on right edge (= inner edge)
           V1 = (i-M-0.5)/M1;
           W0(i,j) = 1-V1;
           W1(i,j) = V1;
           %W2(i,j) remains 0
       else
           V = A*([i-0.5;j-0.5]-R0); %all components of V are <1 because search domain is minimal rectangular enclosure of triangle
           if V(1)>0 && V(2)>0 %detect remaining points inside triangle (1-V(1)-V(2)>0 in current search region)
               W0(i,j) = 1-V(1)-V(2);
               W1(i,j) = V(1);
               W2(i,j) = V(2);
           end
       end
   end
end

%Left-bottom rectangle:
A = [R1-R0,R6-R0]^(-1); %R1/R6 are 1st/2nd neighbor points
for i=1:M
   for j=N2+1:N
       if (2*i-1)*N1-(2*(j-N2)-1)*M1==0 %detect points on left edge (= outer edge)
           V2 = (i-0.5)/M1;
           %W0(i,j) remains 0
           W1(i,j) = 0.5*(1-V2); %half weight on outer edge
           W2(i,j) = 0.5*V2; %half weight on outer edge
       elseif ~((2*(M-i+1)-1)*N1-(2*(j-N2)-1)*M2==0) %detect remaining points not on right edge (= inner edge)
           V = A*([i-0.5;j-0.5]-R0); %all components of V are <1 because search domain is minimal rectangular enclosure of triangle
           if V(1)>0 && 1-V(1)-V(2)>0 %detect remaining points inside triangle(V(2)>0 in current search region)
               W0(i,j) = 1-V(1)-V(2);
               W1(i,j) = V(1);
               W2(i,j) = V(2);
           end
       end
   end
end

end