use std::ops::{Index, IndexMut};
use rand::Rng;
use std::time::Instant;
use rayon::prelude::*;

type Element = f64;

#[derive(Debug, Clone, PartialEq)]
pub struct Matrix {
    n: usize,
    values: Vec<Element>,
}

impl Matrix {
    // Constructeur
    pub fn new(n: usize, values: Vec<Element>) -> Self {
        assert_eq!(values.len(), n * n, "Le vecteur doit contenir n^2 éléments");
        Matrix { n, values }
    }

    // Matrice aléatoire
    pub fn random(n: usize) -> Self {
        let mut rng = rand::thread_rng();
        let values: Vec<Element> = (0..n * n).map(|_| rng.gen_range(-1.0..1.0)).collect();
        Matrix::new(n, values)
    }

    // 1. VERSION NAÏVE (i, j, k)
    pub fn multiply_naive(a: &Matrix, b: &Matrix) -> Matrix {
        let n = a.n;
        let mut c = Matrix::new(n, vec![0.0; n * n]);
        for i in 0..n {
            for j in 0..n {
                for k in 0..n {
                    c[(i, j)] += a[(i, k)] * b[(k, j)];
                }
            }
        }
        c
    }

    // 2. VERSION VECTORISÉE / INTERCHANGE (i, k, j)
    pub fn multiply_vectorized(a: &Matrix, b: &Matrix) -> Matrix {
        let n = a.n;
        let mut c = Matrix::new(n, vec![0.0; n * n]);
        for i in 0..n {
            for k in 0..n {
                let aik = a[(i, k)];
                for j in 0..n {
                    c[(i, j)] += aik * b[(k, j)];
                }
            }
        }
        c
    }

    // 3. VERSION CACHE BLOCKING (Tiling)
    pub fn multiply_blocked(a: &Matrix, b: &Matrix, block: usize) -> Matrix {
        let n = a.n;
        let mut c = Matrix::new(n, vec![0.0; n * n]);
        for ii in (0..n).step_by(block) {
            for kk in (0..n).step_by(block) {
                for jj in (0..n).step_by(block) {
                    // Boucles internes sur le bloc
                    for i in ii..std::cmp::min(ii + block, n) {
                        for k in kk..std::cmp::min(kk + block, n) {
                            let aik = a[(i, k)];
                            for j in jj..std::cmp::min(jj + block, n) {
                                c[(i, j)] += aik * b[(k, j)];
                            }
                        }
                    }
                }
            }
        }
        c
    }

    // 4. VERSION PARALLÈLE (Rayon)
    pub fn multiply_parallel(a: &Matrix, b: &Matrix) -> Matrix {
        let n = a.n;
        let mut c_values = vec![0.0; n * n];
        
        c_values.par_chunks_mut(n).enumerate().for_each(|(i, row_c)| {
            for k in 0..n {
                let aik = a[(i, k)];
                for j in 0..n {
                    row_c[j] += aik * b[(k, j)];
                }
            }
        });
        Matrix::new(n, c_values)
    }
}

// Implémentation de l'accès m[(i, j)]
impl Index<(usize, usize)> for Matrix {
    type Output = Element;
    fn index(&self, index: (usize, usize)) -> &Self::Output {
        &self.values[index.0 * self.n + index.1]
    }
}

impl IndexMut<(usize, usize)> for Matrix {
    fn index_mut(&mut self, index: (usize, usize)) -> &mut Self::Output {
        &mut self.values[index.0 * self.n + index.1]
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 3 {
        println!("Usage: cargo run --release <version> <size>");
        return;
    }

    let version = &args[1];
    let n: usize = args[2].parse().unwrap();

    let a = Matrix::random(n);
    let b = Matrix::random(n);
    
    Matrix::multiply_naive(&a, &b);

    let start = Instant::now();
    let _res = match version.as_str() {
        "naive" => Matrix::multiply_naive(&a, &b),
        "vector" => Matrix::multiply_vectorized(&a, &b),
        "blocked" => Matrix::multiply_blocked(&a, &b, 64),
        "parallel" => Matrix::multiply_parallel(&a, &b),
        _ => panic!("Version inconnue"),
    };
    let duration = start.elapsed();
    let flops = 2.0 * (n as f64).powi(3);
    let gflops = flops / duration.as_secs_f64() / 1e9;
    println!("Version: {}, Taille: {}, Temps: {:?}", version, n, duration);
    println!("Performance: {:.2} GFLOPS", gflops);
}