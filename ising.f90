program ising 
use ziggurat
implicit none
logical :: es, ms
integer :: seed, n, i, j, k, L, s, pv, M, dM, pasos, n_write, aceptados
real(8) :: Jx, E, dE, x,r, prob, Temp, E_avg, E2_avg, M_avg, M2_avg, B !, p_vec(2)
integer, allocatable :: a(:,:)

Jx = 1.0

![NO TOCAR] Inicializa generador de número random

    inquire(file='seed.dat',exist=es)
    if(es) then
        open(unit=10,file='seed.dat',status='old')
        read(10,*) seed
        close(10)
        ! print *,"  * Leyendo semilla de archivo seed.dat"
    else
        seed = 24583490
    end if

    call zigset(seed)
![FIN NO TOCAR]    


!   Leer variables del archivo input.dat
    open(unit=11,file='input.dat',action='read',status='old')
    read(11,*) 
    read(11,*) L, pasos, Temp, B
    close(11)

    n_write = L*L
    !n_write = 1
    allocate(a(0:L+1, 0:L+1))

! Chequear si existe matriz.dat, y cargarla como configuracion inicial
    inquire(file='matriz.dat',exist=ms)
    if(ms) then
        print *,"  * Leyendo configuracion inicial de matriz.dat"
        open(unit=12,file='matriz.dat',status='old')
        read(12,*) a(1:L, 1:L)
        close(12)
        
    else
    ! Si no hay matriz inicial, inicializar con 1 y -1 aleatorios
        print *,"  * Inicializando configuracion aleatoria"
        do j = 1, L
            do i = 1, L
                x = uni()
                if (x <  0.5 ) then
                    a(i,j) = 1
                else
                    a(i,j) = -1
                end if
            end do
        end do

    end if

    ! Condiciones periodicas de contorno
    call cpc()
    
! Calcular la energia y magnetizacion de la matriz
    E=0.0
    M=0
    do j = 1, L
        do i = 1, L
            s = a(i,j)
            pv = a(i+1,j)+a(i,j+1)+a(i-1,j)+a(i,j-1)
            E = E - Jx * s * pv - 2 * B * s     ! Sumo dos veces la parte de campo magnetico porque al final divido por 2
            M = M + s
        end do
    end do
    ! Cuento 2 veces las energias
    E = E/2

    ! Inicializo acumuladores para calcular promedios
    E_avg = E
    E2_avg = E*E
    M_avg = dble(M)
    M2_avg = dble(M*M)
    ! Numero de datos guardados. Será aprox. pasos / n_write
    n = 1
! Algoritmo Metropolis

    ! Archivo para grabar los datos de E y M
    open(unit=13,file='output.dat',action='write',status='replace')

    
    aceptados = 0
    do k = 1, pasos
        i = floor(1 + uni()*L)
        j = floor(1 + uni()*L)
        s = a(i, j)
        pv = a(i+1,j)+a(i,j+1)+a(i-1,j)+a(i,j-1)
        dE = 2*s*pv*Jx + 2*B*s
        dM = -2*s

        if (dE <= 0) then
            a(i, j) = -s
            aceptados = aceptados + 1
        else
            r = uni()
            prob = exp(-dE/Temp)
            if (r < prob) then
                a(i, j) = -s
                aceptados = aceptados + 1
            else
                dE = 0
                dM = 0
            end if
        end if

        ! Condiciones periodicas de contorno
        call cpc()

        ! Calculo la nueva energia y magnetizacion, y actualizo los acumuladores
        E = E + dE
        M = M + dM
        
        ! Grabo 1 dato de E y M cada n_write iteraciones y la fraccion de flips aceptados
        if (mod(k,n_write)==0) then
            write(13,*) E, M, dble(aceptados)/dble(k)
            ! Actualizo los promedios cada n_write iteraciones
            M_avg = M_avg + M
            M2_avg = M2_avg + M*M
            E_avg = E_avg + E
            E2_avg = E2_avg + E*E
            ! Cuento el numero de datos acumulados para calcular los promedios
            n = n + 1
        end if

    end do

    close(13)

! Divido por el numero de datos guardados para obtener promedios
    E_avg = E_avg / n
    E2_avg = E2_avg / n
    M_avg = M_avg / n
    M2_avg = M2_avg / n

! Guardo los promedios en un archivo
    open(unit=14,file='averages.dat',action='write',status='replace')
    write(14,*) 'E     E2     M     M2     Aceptados'
    write(14, *) E_avg, E2_avg, M_avg, M2_avg, dble(aceptados)/dble(k)
    close(14) 

! Guardar la ultima matriz en un archivo

    open(unit=12,file='matriz.dat',action='write',status='replace')
    
    do i= 1, L
        do j = 1, L
            write(12,'(I3)', advance='NO') a(i,j)
        end do
        write(12,*) 

    end do
    close(12) 

![No TOCAR]
! Escribir la última semilla para continuar con la cadena de numeros aleatorios 

    open(unit=10,file='seed.dat',status='unknown')
    seed = shr3() 
    write(10,*) seed
    close(10)
![FIN no Tocar]        


    contains
        ! Rutina que implementa las condiciones periodicas de contorno
        subroutine cpc()
            
            a(0,:) = a(L,:)
            a(L+1,:) = a(1,:)
            a(:,0) = a(:, L)
            a(:,L+1) = a(:, 1)
        
        end subroutine  

end program ising
