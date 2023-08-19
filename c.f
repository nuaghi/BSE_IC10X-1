      IMPLICIT REAL*8 (A-H, L-Z)
      real*8 porb1,md1,dt1
      open(4,file='lps0.dat',status='unknown')
      do i = 1,2880
      read(4,*)porb1,md1,dt1            
      if(dt1.ge. 1.0d9)then
      write(101,11)porb1,md1,dt1
      elseif(dt1.ge.1.0d8)then
      write(102,11)porb1,md1,dt1
      elseif(dt1.ge.1.0d7)then
      write(103,11)porb1,md1,dt1
      elseif(dt1.ge.1.0d6)then
      write(104,11)porb1,md1,dt1
      elseif(dt1.ge.1.0d5)then
      write(105,11)porb1,md1,dt1
      elseif(dt1.ge.1.0d4)then
      write(106,11)porb1,md1,dt1
      elseif(dt1.lt.1.0d4.and.dt1.gt.0)then
      write(107,11)porb1,md1,dt1
      endif
      enddo
11    format(2f8.3,1E12.2)      
      end
