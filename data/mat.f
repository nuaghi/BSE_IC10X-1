      IMPLICIT REAL*8 (A-H, L-Z)
      real*8 porb,m,N,N1,dt,a(100,100)
      open(4,file='hchnwd.dat',status='unknown')
      open(1001,file='hchnwd.end',status='unknown')            
      do i = 1,100
      do j = 1,100
      read(4,*)m,porb,N
!      if(m.le.3.or.porb.le.1) N = 0.0
      N = 1.00*N
      a(i,j) = N
      if(m.ge.-10.and.m.le.1000.0)then            
      n1= n+n1
      write(*,*) N1
      endif
      
      enddo
      enddo
      do j = 1,100
      do i = 1,100
      N = a(i,j)
      if(i.lt.100)then
      write(1001,11,advance="no") N
      elseif(i.eq.100)then
      write(1001,11) N      
      endif
      enddo
      enddo
     
11    format(100E10.2)
      end      
