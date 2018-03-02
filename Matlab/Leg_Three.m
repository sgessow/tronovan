for theta=0:0.1:8*pi
    %Location of Motor
    M=[0,0];
    %Location of other fixed point
    F=[4,0];
    %Lengths of bars in the linkage (clockwise)
    a=1;
    b=4;
    c=1;
    alpha=1*(pi/2-1*imag(acos((F(1)-M(1))/2*b)));
    %Define the other points based on the line lengths
    A=[a*cos(theta),a*sin(theta)];
    B=[A(1)+b*cos(alpha),A(2)+b*sin(alpha)];
    C=[B(1)+c,B(2)];
    %Length of flexture
    Length=sqrt((F(1)-C(1))^2+(F(2)-C(2))^2);
    %Plot line MA
    plot([M(1), A(1)], [M(2), A(2)],'ro-');hold on;
    %Plot line AB
    plot([A(1), B(1)], [A(2), B(2)],'ro-');hold on;
    %Plot line BC
    plot([B(1), C(1)], [B(2), C(2)],'ro-');hold on;
    %Plot line CF
    plot([C(1), F(1)], [C(2), F(2)],'ro-');hold off; 
    hold on;
    str="Length: " + num2str(Length);
    text(3,1,str);
    hold off;
    axis([-2 5 -6 2]);
    pause(0.1);
end