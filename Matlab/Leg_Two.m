degrees=0:0.1:2*pi;
traceXC=zeros(1,length(degrees));
traceYC=zeros(1,length(degrees));
traceXB=zeros(1,length(degrees));
traceYB=zeros(1,length(degrees));
traceMinX=zeros(1,length(degrees));
traceMinY=zeros(1,length(degrees));
%Location of Ground
Ground=-4.25;
count=0;
for theta=degrees
    count=count+1;
    %Location of Motor
    M=[0,0];
    plot(M(1),M(2),'b-o','MarkerFaceColor','b'); hold on;
    %Location of other fixed point
    F=[0.1,-2];
    plot(F(1),F(2),'b-o','MarkerFaceColor','b'); hold on;
    %Lengths of bars in the linkage (clockwise)
    a=1;
    b=4;
    c=.5;
    %Define the other points based on the line lengths
    A=[a*cos(theta),a*sin(theta)];
    B=((F-A)/norm(F-A))*b+A;
    C=computeFoot(A,B,c);
    %update trace plots
    traceXC(count)=C(1);
    traceYC(count)=C(2);
    traceXB(count)=B(1);
    traceYB(count)=B(2);
    if abs(C(1))>abs(B(1))
        traceMinX(count)=C(1);
        traceMinY(count)=C(2);
    else
        traceMinX(count)=B(1);
        traceMinY(count)=B(2);
    end
        
    %Plot line MA
    plot([M(1), A(1)], [M(2), A(2)],'r-');hold on;
    %Plot line AB
    plot([A(1), B(1)], [A(2), B(2)],'r-');hold on;
    %Plot line BC
    plot([B(1), C(1)], [B(2), C(2)],'r-');hold on;
    %Plot trace of foot
    plot(traceXB(1:count),traceYB(1:count),'g.');hold on;
    plot(traceXC(1:count),traceYC(1:count),'b.');hold on;
    plot(traceMinX(1:count),traceMinY(1:count),'m-');hold on;
    %Plot Horizantal line
    line([-10,10],[Ground,Ground]);hold off;
    axis([-4 4 -6 2]);
    pause(0.05);
end
T=computeTimeOnGround(traceMinY(1:count),Ground)

%Function Section
function C=computeFoot(A,B,lengthOfFoot)
 C_dir=cross([B(1)-A(1),B(2)-A(2),0],[0,0,1]);
 C=C_dir(1:2)/norm(C_dir(1:2))*-lengthOfFoot+B;
end
function Time_On_Ground = computeTimeOnGround(PositionVector,floorPos)
pointsOnGround=0;
totalTime=length(PositionVector);
for pos = PositionVector
    if pos<=floorPos
        pointsOnGround=pointsOnGround+1;
    end
end
Time_On_Ground=double(pointsOnGround)/double(totalTime)*100;
end

    
    