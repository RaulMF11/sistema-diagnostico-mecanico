<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Services\DiagnosticoService;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

// Ruta de prueba para verificar conexión Laravel → IA
Route::post('/prueba-ia', function (Request $request) {
    $service = new DiagnosticoService();

    $datos = $request->all(); // toma los datos enviados por POST

    return $service->generarDiagnostico($datos);
});
